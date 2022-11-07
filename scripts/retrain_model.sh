#!/bin/bash

timestamp=$(date +%Y%m%d%H%M%S)
output_folder="../backend/model_outputs_$timestamp"
data_location="./data/arxiv-metadata-oai-snapshot.json" # user config

mkdir -p "$output_folder/model_outputs"

python3 generate_soft_labels.py \
--data_location="$data_location" \
--output_location="$output_folder"