# Multipunct

Train models to restore punctuation and capitalization for texts in different languages. Based on [NeMo project](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/stable/nlp/punctuation_and_capitalization.html).

## Download dataset

At first you need to download the dataset with the texts in desired language. You can use the Tatoeba dataset for that purpose. It has fairly enough punctuation marks.

Use the following code to get Tatoeba dataset:

```
python3 ./get_tatoeba.py --data_dir ./dataset --lang rus
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
python3 ./prepare_data.py --data_dir ./dataset --num_samples 10000 --percent_dev 0.2
```

## Training the model

And finally we will train the model. You can train the model locally or use the following notebook (it's a fixed NeMo's Jupyter nb).

- [train.ipynb](train.ipynb)
- Choose base BERT model in PRETRAINED_BERT_MODEL

  - [DeepPavlov/distilrubert-tiny-cased-conversational-v1](https://huggingface.co/DeepPavlov/distilrubert-tiny-cased-conversational) used in this example notebook.

### Colab

- Try to train in [Colab](https://colab.research.google.com/drive/1p6K3FwmRxEO_NIP6ihsCAjFS2bX1pX6o?usp=sharing)

## Further improvements

- To increase the quality please make sure that your dataset is balanced in terms of punctuation ratio.
- Adjust the training parameters.
- Try to choose different pretrained models (you can choose any BERT model from [huggingface](https://huggingface.co/)).

## Examples

```python
queries = [
        'меня зовут сергей а как тебя',
        'подскажи пожалуйста сегодня вторник или среда',
        'закрой за мной дверь я ухожу'
    ]

inference_results = model.add_punctuation_capitalization(queries)

for query, result in zip(queries, inference_results):
    print(f'Query   : {query}')
    print(f'Combined: {result.strip()}\n')
```

```python
Query   : меня зовут сергей а как тебя
Combined: Меня зовут Сергей. А как тебя?

Query   : подскажи пожалуйста сегодня вторник или среда
Combined: Подскажи, пожалуйста, сегодня вторник или среда.

Query   : закрой за мной дверь я ухожу
Combined: Закрой за мной дверь. Я ухожу.
```
