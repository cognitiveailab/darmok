#!/bin/bash

#    --model_name_or_path /tmp/tst-translation \
#python examples/pytorch/seq2seq/run_translation.py \
python3 run_translation.py \
    --model_name_or_path t5-base \
    --do_train \
    --do_eval \
    --do_predict \
    --source_lang en \
    --target_lang tam \
    --source_prefix "translate English to Tamarian: " \
    --output_dir /tmp/tst-translation \
    --per_device_train_batch_size=1 \
    --per_device_eval_batch_size=1 \
    --num_train_epochs=30 \
    --save_total_limit=2 \
    --save_steps=10000 \
    --evaluation_strategy=epoch \
    --overwrite_output_dir \
    --train_file=/home/peter/github/darmok/data/july14/fold5/train.json \
    --validation_file=/home/peter/github/darmok/data/july14/fold5/dev.json \
    --test_file=/home/peter/github/darmok/data/july14/fold5/test.json \
    --predict_with_generate \
    --num_beams=4
    
#   --dataset_name wmt16 \    
#   --dataset_config_name ro-en \    
#--do_train \
