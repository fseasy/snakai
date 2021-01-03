# -*- coding: utf-8 -*-
"""snake executor strategy
control how to move the snake
"""
import enum

from .. import snake_state_machine as ssm


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

    @classmethod
    def effective_direction2action(cls, d: ssm.Direction) -> 'Action':
        """direction -> action
        """
        _D = ssm.Direction
        _m = {
            _D.LEFT: cls.MOVE_LEFT,
            _D.RIGHT: cls.MOVE_RIGHT,
            _D.UP: cls.MOVE_UP,
            _D.DOWN: cls.MOVE_DOWN
        }
        if d not in _m:
            raise ValueError(f"[{d}] not supported for direction->action")
        return _m[d]


class Strategy(object):
    """strategy base
    """
    def gen_next_action(self, game_state) -> Action:
        """generating next action according to the game-state
        """
        raise NotImplementedError("should impl it")
