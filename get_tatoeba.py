import argparse
import logging
import os
import requests


URL = "https://downloads.tatoeba.org/exports/sentences.csv"


def maybe_download_file(destination: str):
    if not os.path.exists(destination):
        file = requests.get(URL, allow_redirects=True)
        with open(destination, mode="wb") as file_output:
            file_output.write(file.content)
    else:
        logging.info(f"{destination} found. Skipping download")


def get_lang_sentences(filepath, lang):
    txt_path = os.path.join(args.data_dir, "sentences.txt")
    os.path.join(args.data_dir, "sentences.csv")
    with open(filepath, "r", encoding="utf-8") as fin:
        with open(txt_path, "w", encoding="utf-8") as fout:
            for i, line in enumerate(fin.readlines()):
                line = line.split("\t")
                if line[1] == lang:
                    fout.write(line[2].strip() + "\n")
    logging.info(f"{i} files were added into senteces.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare dataset")
    parser.add_argument("--data_dir", required=True, type=str)
    parser.add_argument("--lang", required=True, type=str)
    args = parser.parse_args()

    if not os.path.exists(args.data_dir):
        os.makedirs(args.data_dir)

    dataset = os.path.join(args.data_dir, "sentences.csv")
    maybe_download_file(dataset)
    get_lang_sentences(dataset, args.lang)
