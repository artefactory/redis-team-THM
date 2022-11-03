#!/bin/bash

declare -a cutoffs=(200811 200812 200901 200902 200903 200904 200905 200906 200907)
# 1991 to 2022

# Model names (see https://huggingface.co/spaces/mteb/leaderboard)
# - sentence-transformers/all-mpnet-base-v2
# - sentence-transformers/all-MiniLM-L6-v2
# - sentence-transformers/all-MiniLM-L12-v2

filename="output"

for cutoff in "${cutoffs[@]}"
do
    path="arxiv/cutoff=$cutoff"
    mkdir -p "$path"

    if [ -f "$path/$filename.pkl" ]
    then
        echo "$path already exists."
    else
        PYTHONPATH=../backend python3 generate_index.py \
        --year_month="$cutoff" \
        --input_path="arxiv-metadata-oai-snapshot.json" \
        --output_path="$path/$filename.pkl" \
        --model_name="sentence-transformers/all-MiniLM-L12-v2"
    fi

    PYTHONPATH=../backend python3 load_data.py \
    --concurrency_level=2 \
    --separator="|"  \
    --vector_size=384 \
    --reset_db=False \
    --embeddings_path="$path/$filename.pkl"
done