#!/bin/sh

python train.py \
    --win_width 9 \
    --win_height 9 \
    --learning_rate 0.1 \
    --discount 0.9 \
    --init_exploration_rate 0.5 \
    --exploration_decay_iter 40 \
    --total_iter 10000 \
    --without_ui \
    --model_save_path output/ql_strategy.pickle 