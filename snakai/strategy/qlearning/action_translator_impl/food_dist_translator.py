# -*- coding: utf-8 -*-
"""food distance translator
"""
import enum

class FoodDistState(enum.Enum):
    ZERO = "0"
    POSITIVE = "positive"
    NEGATIVE = "negative"


class FoodDistTranslator(object):
    """food distance translator"""
    def __init__(self):
        self._states = [s.value() for s in FoodDistState()]
    
    def translate(self, dist: int) -> str:
        if dist == 0:
            return FoodDistState.ZERO.value
        elif dist > 0:
            return FoodDistState.POSITIVE.value
        else:
            return FoodDistState.NEGATIVE.value
    
    @property