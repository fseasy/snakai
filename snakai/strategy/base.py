# -*- coding: utf-8 -*-
"""snake executor strategy
control how to move the snake
"""
import enum


class Action(enum.Enum):
    """strategy action
    """
    MOVE_LEFT = 0
    MOVE_RIGHT = 1
    MOVE_UP = 2
    MOVE_DOWN = 3

    EXIT = 4
    PAUSE_RESUME = 5
    IDLE = 6


class Strategy(object):
    """strategy base
    """
    def gen_next_action(self, game_state) -> Action:
        """generating next action according to the game-state
        """
        raise NotImplementedError("should impl it")