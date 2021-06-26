# -*- coding: utf-8 -*-
"""snake executor strategy
control how to move the snake
"""
import enum

from .. import snake_state_machine as ssm


class Action(enum.Enum):
    """strategy action
    """
    MOVE_LEFT = enum.auto()
    MOVE_RIGHT = enum.auto()
    MOVE_UP = enum.auto()
    MOVE_DOWN = enum.auto()

    EXIT = enum.auto()
    PAUSE_RESUME = enum.auto()
    IDLE = enum.auto()

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
    def gen_next_action(self, game_state: ssm.SnakeStateMachine) -> Action:
        """generating next action according to the game-state
        """
        raise NotImplementedError("should impl it")

    def update(self, game_state: ssm.SnakeStateMachine):
        """update strategy if needed
        default is do noting.
        """
        return

    def start_new(self, game_state: ssm.SnakeStateMachine):
        """start new strategy
        default do noting
        """
        return