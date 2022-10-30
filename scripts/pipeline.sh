#!/bin/bash

declare -a cutoffs=(200811)
# 1991 to 2022

# declare -a models=(
#     "sentence-transformers/all-mpnet-base-v2"
#     "sentence-transformers/all-MiniLM-L12-v2"
# )

for cutoff in "${cutoffs[@]}"
do
    python3 generate_index.py \
        --year_month="$cutoff" \
        --input_path="arxiv-metadata-oai-snapshot.json" \
        --output_path="arxiv/cutoff=$cutoff/output.pkl" \
        --model_name="sentence-transformers/all-MiniLM-L12-v2"
done

# python3 load_data.py \
#     --concurrency_level=2 \
#     --separator="|"  \
#     --reset_db=False