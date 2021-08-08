#!python3 
# -*- coding: utf-8 -*-
"""train q-learning strategy
"""
import argparse
import logging
import pathlib
import time
import pickle
import tqdm

from snakai.strategy.qlearning import strategy
from snakai import snake_state_machine as ssm
from snakai import curses_game
from snakai.util import logger as logger_module


logger = logging.getLogger("snakai")

def train_without_ui(args):
    """train without ui"""
    ql_strategy = strategy.QLearningStrategy(is_infer=False, 
        train_args=args,
        infer_args=None)
    
    state = ssm.SnakeStateMachine(width=args.win_width, height=args.win_height)
    
    for train_iter in tqdm.tqdm(range(args.total_iter)):
        state.new_state()
        while state.is_state_ok():
            action = ql_strategy.gen_next_action(state, None)
            direction = action.to_direction()
            state.update_state(direction)
            ql_strategy.update(state)
        ql_strategy.clear4next(state)
        if (train_iter + 1) % 500 == 0:
            logger.info("train iter %d, state score: %d, steps: %d, table-filling ratio: %.2f%%", 
                train_iter, state.score, state.steps, ql_strategy.table_filling_ratio() * 100)
    pathlib.Path(args.model_save_path).parent.mkdir(parents=True, exist_ok=True)
    with open(args.model_save_path, mode="wb") as outputf:
        pickle.dump(obj=ql_strategy, file=outputf)
    print("table filling strategy", ql_strategy._qtable.table_filling_ratio())


def train_with_ui(args):
    """train Q-Learning with UI monitor
    """
    ql_strategy = strategy.QLearningStrategy(is_infer=False, train_args=args, infer_args=None)
    state = ssm.SnakeStateMachine(width=args.win_width, height=args.win_height)
    ui = curses_game.SnakeUIFramework(width=args.win_width, height=args.win_height)
    state_render = curses_game.SnakeStateRender(ui)

    for train_iter in range(args.total_iter):
        logger.info("iter: %s", train_iter)
        with ui.active_env():
            ui.init_window()
            state.new_state()
            state_render.render_init_state(state)
            while state.is_state_ok():
                action = ql_strategy.gen_next_action(state, None)
                direction = action.to_direction()
                state.update_state(direction)
                ql_strategy.update(state)
                state_render.render_updated_state(state)
                ui.refresh()
                # time.sleep(0.001)
            ql_strategy.clear4next(state)
            logger.info("state score: %d, steps: %d", state.score, state.steps)
    
    pathlib.Path(args.model_save_path).parent.mkdir(parents=True, exist_ok=True)
    with open(args.model_save_path, mode="wb") as outputf:
        pickle.dump(obj=ql_strategy, file=outputf)
    print("table filling strategy", ql_strategy._qtable.table_filling_ratio())

def main():
    """main process for train"""
    logger_module.init_logger(name="snakai", fpath="/dev/shm/snakai_train_log.log", level=logging.INFO)
    parser = argparse.ArgumentParser(description="train ql learning strategy")
    parser.add_argument("--win_width", type=int, help="window width", default=60)
    parser.add_argument("--win_height", type=int, help="window height", default=20)
    parser.add_argument("--learning_rate", "-lr", type=float, help="learning rate", default=0.1)
    parser.add_argument("--discount", type=float, help="discount", default=0.9)
    parser.add_argument("--init_exploration_rate", type=float, 
        help="initial exporation rate", default=0.5)
    parser.add_argument("--exploration_decay_iter", "-edi", type=int, 
        help="how many iterations after exploration decay to zero", default=20)
    parser.add_argument("--seed", type=int, help="random seed", default=1234)
    parser.add_argument("--total_iter", "-ti", type=int, help="training iterations", default=20)
    parser.add_argument("--without_ui", action="store_true", help="whether diable ui")
    parser.add_argument("--model_save_path", "-o", help="where to save model", required=True)
    args = parser.parse_args()

    if args.without_ui:
        train_without_ui(args)
    else:
        train_with_ui(args)


if __name__ == "__main__":
    main()