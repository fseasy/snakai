#!python3
# -*- coding: utf-8 -*-
"""run game
"""
import argparse
import logging

from snakai import strategy as strategy_module
from snakai import curses_game


def main():
    """main program
    """
    logging.basicConfig(level=logging.INFO)
    args = _parse_args()
    game_exe = curses_game.CursesSnakeGameExe(win_width=args.width, win_height=args.height, 
        speed="slow")
    strategy = strategy_module.init_strategy(args.strategy, game_exe.curses_ui, game_exe.frame_time)    
    game_exe.run(strategy)


def _parse_args():
    parser = argparse.ArgumentParser(description="Snakai executor, currently use curses as game body")
    parser.add_argument("--strategy", "-s", choices=strategy_module.get_names(), default="manual", 
        help="which strategy to execute")
    parser.add_argument("--width", default=60, type=int, help="curses window width")
    parser.add_argument("--height", default=20, type=int, help="curses window height")
    return parser.parse_args()


if __name__ == "__main__":
    main()
