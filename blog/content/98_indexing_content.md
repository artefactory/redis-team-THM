Title: Indexing Contents to Redis
Date: 2022-11-04 11:25
Modified: 2022-11-04 11:25
Category: MLOps
Tags: python, redis, mlops
Slug: indexing-contents
Authors: Michel Hua
Summary: The THM CLI

# Reindexing contents

If you want to index your own private database of documents, you can reuse the scripts

## Generate the index

To generate index for a specific cutoff you can just run this script, choosing you JSON file containing your corpus, the output where to store index file in Pickle format, and the model name to encode your sentences.

This task can be performed on one month of arXiv data on a regular desktop, but you might want to schedule it using tools like [Airflow](https://github.com/apache/airflow).

```sh
% ./generate-index.py --help


NAME
    generate_index.py - Generate Embeddings and Create a File Index.

SYNOPSIS
    generate_index.py YEAR_MONTH <flags>

DESCRIPTION
    Generate Embeddings and Create a File Index.

POSITIONAL ARGUMENTS
    YEAR_MONTH

FLAGS
    --input_path=INPUT_PATH
        Default: 'arxiv-metadata-o...
    --output_path=OUTPUT_PATH
        Default: 'arxiv_embeddings_10000...
    --model_name=MODEL_NAME
        Default: 'sentence-...
```

To cold start your database you can also run the [`single-gpu-arxiv-embedding`](https://github.com/artefactory/redis-team-THM/blob/main/datascience/single-gpu-arxiv-embeddings.ipynb) Jupyter Notebook on Saturn Cloud. Using a `T4-XLarge 4-cores`, `saturn-python-rapids` image, the data from the historical 2 million papers was indexed in less than 5 minutes.

## Load the index to Redis

```sh
% ./load_data.py --help


NAME
    load_data.py - Load the Embedding Index to Redis.

SYNOPSIS
    load_data.py <flags>

DESCRIPTION
    Load the Embedding Index to Redis.

FLAGS
    --concurrency_level=CONCURRENCY_LEVEL
        Type: int
        Default: 2
    --separator=SEPARATOR
        Type: str
        Default: '|'
    --reset_db=RESET_DB
        Type: bool
        Default: False
    --embeddings_path=EMBEDDINGS_PATH
        Type: str
        Default: ''
    --vector_size=VECTOR_SIZE
        Type: int
        Default: 768
```
