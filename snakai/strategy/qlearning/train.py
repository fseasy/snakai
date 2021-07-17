#!python3 
# -*- coding: utf-8 -*-
"""train q-learning strategy
"""
import argparse
import logging

from snakai.strategy.qlearning import strategy
from snakai import snake_state_machine as ssm
from snakai.util import logger as logger_module


logger = logging.getLogger("snakai")

def train_with_ui(args):
    """train with ui"""
    ql_strategy = strategy.QLearningStrategy(is_infer=False, 
        train_args=args,
        infer_args=None)
    
    state = ssm.SnakeStateMachine(width=args.win_width, height=args.win_height)
    
    for train_iter in range(args.total_iter):
        state.new_state()
        while state.is_state_ok():
            action = ql_strategy.gen_next_action(state)
            direction = action.to_direction()
            state.update_state(direction)
            ql_strategy.update(state)
        # state ended, should do last update for the final state
        ql_strategy.update(state)
        ql_strategy.clear4next(state)
        logger.info("iter: %s", train_iter)
        

def main():
    """main process for train"""
    logger_module.init_logger(name="snakai")
    parser = argparse.ArgumentParser(description="train ql learning strategy")
    parser.add_argument("--win_width", type=int, help="window width", default=60)
    parser.add_argument("--win_height", type=int, help="window height", default=20)
    parser.add_argument("--learning_rate", type=float, help="learning rate", default=0.1)
    parser.add_argument("--discount", type=float, help="discount", default=0.9)
    parser.add_argument("--init_exploration_rate", type=float, 
        help="initial exporation rate", default=0.5)
    parser.add_argument("--exploration_decay_iterations", type=int, 
        help="how many iterations after exploration decay to zero", default=20)
    parser.add_argument("--seed", type=int, help="random seed", default=1234)
    parser.add_argument("--total_iter", type=int, help="training iterations", default=20)
    args = parser.parse_args()

    train_with_ui(args)


if __name__ == "__main__":
    main()