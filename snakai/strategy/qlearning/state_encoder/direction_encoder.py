# -*- coding: utf-8 -*-
"""direction encoder
"""

from .encoder_base import EncoderBase
from snakai.snake_state_machine import Direction as D


class DirectionEncoder(EncoderBase):
    """direction encoder.
    direct use the snake direction
    """
    def __init__(self):
        # only use effective 4 directions
        self._id2states = [D.UP, D.DOWN, D.LEFT, D.RIGHT]
        self._state2id = {_s: _i for (_i, _s) in enumerate(self._id2states)}

    def encode(self, game_state) -> int:
        return self._state2id[game_state.direction]

    def readable_state(self, state_id) -> list:
        return [self._id2states[state_id].name,]

    @property
    def ids(self):
        return self._state2id.values()