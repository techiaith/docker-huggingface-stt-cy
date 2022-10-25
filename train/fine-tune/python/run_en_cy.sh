#!/bin/bash

# this is refering to a Python file that contains values
# shown in cv_version.template.py
export CV_CONFIG_FILE='cv_version_11_en_cy'


# "facebook/wav2vec2-xls-r-1b"
pre_trained_model='facebook/wav2vec2-large-xlsr-53'

session_date=$(date '+%Y-%m-%d_%H:%M:%S')
session_name=${pre_trained_model//\//_}__${session_date}

training_dir="/root/sessions/"${session_name}

set -x

accelerate launch run.py \
    --session-id="${session_name}" \
    --training-dir="${training_dir}" \
    --training-split-name="train+validation" \
    --test-split-name="test" \
    --language="cy" \
    --train-wav2vec2 \
    --no-train-kenlm \
    --no-optimize-kenlm \
    --pre-trained-model-name="${pre_trained_model}" \
    --oscar-text-corpus-name="unshuffled_deduplicated_cy" 


python3 evaluate.py --model_path="${training_dir}"

python3 evaluate.py --model_path="${training_dir}" --test-split-name="test_cy"

python3 evaluate.py --model_path="${training_dir}" --test-split-name="test_en"

python3 test.py --model_path="${training_dir}" --test_csv /data/corpws-profi-adnabod-lleferydd/data/trawsgrifio/clips.csv
