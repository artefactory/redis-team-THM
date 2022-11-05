Title: Indexing Contents to Redis
Date: 2022-11-04 11:25
Modified: 2022-11-04 11:25
Category: THM Indexing
Tags: python, redis, mlops
Slug: indexing-contents
Authors: Michel Hua
Summary: Indexing Contents to Redis

# Reindexing contents

If you want to index your own private database of documents, you can reuse the scripts

## Generating the index

To generate index for a specific cutoff you can run this script. You must specify a JSON file containing your corpus. the output where to store index file (in Pickle format), and the model name to encode your sentences.

This task can be performed on one month of arXiv data on a regular desktop, you might want to schedule it using tools like [Airflow](https://github.com/apache/airflow).

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

## Loading the index to Redis

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


## Using a basic pipeline

[`pipeline.sh`](https://github.com/artefactory/redis-team-THM/blob/main/scripts/pipeline.sh) takes a list of cutoffs and a model name for embeddings encoding. You can track progress thanks to [`tqdm/tqdm`](https://github.com/tqdm/tqdm).

```sh
% ./pipeline.sh
2022-11-03 19:36:13.555 | INFO     | __main__:run:39 - Reading papers for 200907...
2022-11-03 19:36:30.045 | INFO     | __main__:run:45 - Creating embeddings from title and abstract...
2022-11-03 19:36:30.045 | INFO     | __main__:run:46 - sentence-transformers/all-MiniLM-L12-v2
100%|██████████████████████████████████████████████████████████████████████████████| 2306/2306 [01:14<00:00, 30.78it/s]
2022-11-03 19:37:44.977 | INFO     | __main__:run:55 - Exporting to pickle file...
2022-11-03 19:37:45.803 | INFO     | __main__:run:111 - TODO False
2022-11-03 19:37:45.804 | INFO     | __main__:load_all_data:64 - Loading papers...
2022-11-03 19:37:46.052 | INFO     | __main__:load_all_data:68 - Writing to Redis...
 87%|███████████████████████████████████████████████████████████████████▊          | 2003/2306 [01:28<00:13, 22.24it/s]
```
