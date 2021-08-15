#!/bin/sh

python train.py \
    --learning_rate 0.01 \
    --discount 0.9 \
    --init_exploration_rate 0.5 \
    --exploration_decay_iter 40 \
    --total_iter 100000 \
    --without_ui \
    --model_save_path output/ql_strategy.pickle 
