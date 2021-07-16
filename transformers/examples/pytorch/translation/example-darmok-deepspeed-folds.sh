#!/bin/bash


export FOLDNUM=$1
export INDIR=/home/pajansen/github/darmok/data/july14/fold${FOLDNUM}/
export OUTDIR=/home/pajansen/github/darmok/models/out-base-ds-fold${FOLDNUM}

echo "FoldNum: $FOLDNUM"; 

#python3 run_translation.py \
deepspeed --num_gpus=1 run_translation.py \
    --model_name_or_path t5-base \
    --do_train \
    --do_eval \
    --do_predict \
    --source_lang en \
    --target_lang tam \
    --source_prefix "translate English to Tamarian: " \
    --max_source_length=128 \
    --max_target_length=128 \
    --output_dir ${OUTDIR} \
    --per_device_train_batch_size=1 \
    --per_device_eval_batch_size=1 \
    --num_train_epochs=30 \
    --save_total_limit=2 \
    --save_steps=10000 \
    --evaluation_strategy=epoch \
    --overwrite_output_dir \
    --train_file=${INDIR}/train.json \
    --validation_file=${INDIR}dev.json \
    --test_file=${INDIR}test.json \
    --predict_with_generate \
    --num_beams=4 \
    --deepspeed ../../../tests/deepspeed/ds_config_zero2.json \
    --fp16 

    
#   --dataset_name wmt16 \    
#   --dataset_config_name ro-en \    
#--do_train \
