# Multipunct

Train models to restore punctuation and capitalization for texts in different languages. Based on [NeMo project](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/stable/nlp/punctuation_and_capitalization.html).

## Download dataset

At first you need to download the dataset with the texts in desired language. You can use the Tatoeba dataset for that purpose. It has fairly enough punctuation marks.

Use the following code to get Tatoeba dataset:

```
python ./get_tatoeba.py --data_dir ./dataset --lang rus
```

Dataset will be downloaded into _dataset_ folder in sentences.csv file. After that the sentences with your language code will be written in **sentences.txt** file.

## Prepare dataset

At the next step we need to prepare the dataset for training.

- Clean sentences
  - Remove the punctuation you don't want to restore
    - Desired chars to restore are in the **CHARS** constant in the _prepare_data.py_ script. Update it if needed.
  - Standartize the punctuation
    - Remove some fancy unicode punctuation with the usual one
- Encode sentences
  - Translate the sentences into something like **OU OO ?O**
    - It's special markup for our model
    - Details are [here](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/stable/nlp/punctuation_and_capitalization.html)
- Split data on train and dev sets

To do that run the following code:

```
python ./prepare_data.py --data_dir ./dataset --num_samples 10000 --percent_dev 0.2
```
