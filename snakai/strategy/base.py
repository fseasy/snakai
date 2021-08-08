# -*- coding: utf-8 -*-
"""snake executor strategy
control how to move the snake
"""
import enum

from .. import snake_state_machine as ssm


class Strategy(object):
    """strategy base
    """
    def gen_next_action(self, _game_state: ssm.SnakeStateMachine, _exe) -> 'Action':
        """generating next action according to the game-state
        exe: Game Executor. 
            we think strategy running not only need the snake game state, and also some Executor Environments.
            so we pass a Game Executor to this.
        """
        raise NotImplementedError("should impl it")

    def update(self, _game_state: ssm.SnakeStateMachine, _exe):
        """update strategy if needed
        default is do noting.
        """
        return

    def clear4next(self, _game_state: ssm.SnakeStateMachine):
        """clear inner temporatory state for next running
        default do noting
        """
        return


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

    def to_direction(self) -> ssm.Direction:
        """action to direction"""
        _D = ssm.Direction
        _m = {
            Action.MOVE_LEFT: _D.LEFT,
            Action.MOVE_RIGHT: _D.RIGHT,
            Action.MOVE_UP: _D.UP,
            Action.MOVE_DOWN: _D.DOWN
        }
        # if no valid, just raise exception
        return _m[self]
