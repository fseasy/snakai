# -*- coding: utf8 -*-
"""encoder base"""

from snakai.snake_state_machine import SnakeStateMachine

class EncoderBase(object):
    """encoder base"""
    def encode(self, game_state: SnakeStateMachine) -> int:
        raise NotImplementedError("impl encode")

    def clear(self):
        pass

    def readable_state(self, state_id: int) -> list:
        raise NotImplementedError("impl readable_state")

    @property
    def ids(self):
        raise NotImplementedError("impl ids")