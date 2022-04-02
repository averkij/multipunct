import argparse
import logging
import os
import random
import re
import string
import requests


CHARS = ".,?!"


def process_sentences(
    in_file: str,
    out_file: str,
    num_samples: int = -1,
    chars_to_restore: str = ".,!?",
    percent_to_cut=0.02,
    num_to_combine: int = 2,
):
    if not os.path.exists(in_file):
        raise FileNotFoundError(f"{in_file} not found.")

    all_except_needed = string.punctuation + "«»—"
    all_except_needed = re.sub(f"[{chars_to_restore}]", "", all_except_needed)
    lines_to_combine = []
    samples_count = 0

    print(
        "delete all punctuation except ["
        + chars_to_restore
        + "]. Delete: "
        + all_except_needed
    )

    with open(in_file, "r", encoding="utf-8") as fin:
        with open(out_file, "w", encoding="utf-8") as fout:
            for i, line in enumerate(fin.readlines()):
                pre_line = line.strip()
                line = line.strip()

                line = (
                    line.replace("...", ".")
                    .replace("…", ".")
                    .replace("—", "—")
                    .replace("―", "—")
                    .replace("?!", "?")
                    .replace("!?", "?")
                )
                line = re.sub("[-‐–]", "-", line)

                for c in all_except_needed:
                    line = line.replace(c, "")

                line = re.sub("[ \t]+", " ", line)

                if i % 1000 == 0:
                    print(pre_line + " → " + line)

                if percent_to_cut > 0:
                    line = line.split()
                    if random.random() < percent_to_cut:
                        line = line[: len(line) // 2]
                    line = " ".join(line)

                if len(lines_to_combine) >= num_to_combine:
                    if samples_count == num_samples:
                        return
                    fout.write(" ".join(lines_to_combine) + "\n")
                    lines_to_combine = []
                    samples_count += 1
                lines_to_combine.append(line)

                if samples_count == num_samples:
                    return

            if len(lines_to_combine) > 0 and (
                samples_count < num_samples or num_samples < 0
            ):
                fout.write(" ".join(lines_to_combine) + "\n")


def split_into_train_dev(
    in_file: str, train_file: str, dev_file: str, percent_dev: float
):
    if not os.path.exists(in_file):
        raise FileNotFoundError(f"{in_file} not found.")

    lines = open(in_file, "r", encoding="utf-8").readlines()
    train_file = open(train_file, "w", encoding="utf-8")
    dev_file = open(dev_file, "w", encoding="utf-8")

    dev_size = int(len(lines) * percent_dev)
    train_file.write(" ".join(lines[:-dev_size]))
    dev_file.write(" ".join(lines[-dev_size:]))


def remove_punctuation(word: str):
    all_punct_marks = string.punctuation + "«»—"
    return re.sub("[" + all_punct_marks + "]", "", word)


def create_text_and_labels(output_dir: str, file_path: str, punct_marks: str = ",.?!"):
    if not os.path.exists(file_path):
        raise ValueError(f"{file_path} not found")

    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.basename(file_path)
    labels_file = os.path.join(output_dir, "labels_" + base_name)
    text_file = os.path.join(output_dir, "text_" + base_name)

    with open(file_path, "r", encoding="utf-8") as f:
        with open(text_file, "w", encoding="utf-8") as text_f:
            with open(labels_file, "w", encoding="utf-8") as labels_f:
                for line in f:
                    line = line.split()
                    text = ""
                    labels = ""
                    for word in line:
                        label = word[-1] if word[-1] in punct_marks else "O"
                        word = remove_punctuation(word)
                        if len(word) > 0:
                            if word[0].isupper():
                                label += "U"
                            else:
                                label += "O"

                            word = word.lower()
                            text += word + " "
                            labels += label + " "

                    text_f.write(text.strip() + "\n")
                    labels_f.write(labels.strip() + "\n")

    print(f"{text_file} and {labels_file} created from {file_path}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare data for training")
    parser.add_argument("--data_dir", required=True, type=str)
    parser.add_argument(
        "--num_samples", default=-1, type=int, help="-1 to use the whole dataset"
    )
    parser.add_argument(
        "--percent_dev", default=0.2, type=float, help="Size of the dev set, float"
    )
    args = parser.parse_args()

    dataset = os.path.join(args.data_dir, "sentences.txt")
    clean_sentences = os.path.join(args.data_dir, "sentences_clean.txt")

    process_sentences(
        dataset,
        clean_sentences,
        args.num_samples,
        CHARS,
    )

    train_file = os.path.join(args.data_dir, "train.txt")
    dev_file = os.path.join(args.data_dir, "dev.txt")

    split_into_train_dev(clean_sentences, train_file, dev_file, args.percent_dev)

    create_text_and_labels(
        args.data_dir, os.path.join(args.data_dir, "train.txt"), CHARS
    )
    create_text_and_labels(args.data_dir, os.path.join(args.data_dir, "dev.txt"), CHARS)