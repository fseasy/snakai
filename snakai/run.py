#!python3
# -*- coding: utf-8 -*-
"""run game
"""
import argparse
import logging

from snakai import strategy as strategy_module
from snakai.curses_game import exe
from snakai.util import logger as logger_module

def main():
    """main program
    """
    logger_module.init_logger("snakai")
    args = _parse_args()
    game_exe = exe.CursesSnakeGameExe(win_width=args.width, win_height=args.height, 
        speed=args.speed)
    strategy = strategy_module.init_strategy(args.strategy, args)    
    game_exe.run(strategy)


def _parse_args():
    parser = argparse.ArgumentParser(description="Snakai executor, currently use curses as game body")
    parser.add_argument("--strategy", "-s", choices=strategy_module.get_names(), default="manual", 
        help="which strategy to execute")
    parser.add_argument("--width", default=60, type=int, help="curses window width")
    parser.add_argument("--height", default=20, type=int, help="curses window height")
    parser.add_argument("--speed", default=exe.GameSpeed.NORMAL.name, choices=exe.GameSpeed.names(), 
        help="curses game speed")
    parser.add_argument("--model_path", help="path to model")
    return parser.parse_args()


if __name__ == "__main__":
    main()
