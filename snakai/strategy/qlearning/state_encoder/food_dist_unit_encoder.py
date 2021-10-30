# -*- coding: utf-8 -*-
"""food distance encoder
"""
import enum

from .encoder_base import EncoderBase


class FoodDistState(enum.Enum):
    ZERO = "0"
    POSITIVE = "positive"
    NEGATIVE = "negative"


class FoodDistUnitEncoder(EncoderBase):
    """food distance unit encoder"""
    def __init__(self):
        self._states = [s.value for s in FoodDistState]
        self._state2id = {_s:_i for (_i, _s) in enumerate(self._states)}

    def encode(self, dist: int) -> str:
        if dist == 0:
            s = FoodDistState.ZERO.value
        elif dist > 0:
            s = FoodDistState.POSITIVE.value
        else:
            s = FoodDistState.NEGATIVE.value
        return self._state2id[s]

    def readable_state(self, state_id) -> list:
        return [self._states[state_id]]

    @property
    def ids(self):
        return self._state2id.values()
