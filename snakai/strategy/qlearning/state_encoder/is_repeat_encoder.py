# coding: utf8
"""Is snake repeat it's path
"""

from .encoder_base import EncoderBase
from snakai.snake_state_machine import SnakeStateMachine

class IsRepeatEncoder(EncoderBase):
    """is repeat"""
    def __init__(self):
        self._previous_score = -1
        self._head_history_pos = set()
        self._states = [False, True]
        self._state2id = {_s: _i for (_i, _s) in enumerate(self._states)}

    def encode(self, game_state: SnakeStateMachine) -> int:
        cur_score = game_state.score
        if cur_score != self._previous_score:
            self.clear()
            self._previous_score = cur_score
        is_repeat = game_state.head in self._head_history_pos
        if not is_repeat:
            self._head_history_pos.add(game_state.head)
        return self._state2id[is_repeat]

    def clear(self):
        self._previous_score = -1
        self._head_history_pos = set()

    def readable_state(self, state_id: int) -> list:
        state = self._states[state_id]
        state_str = "repeat" if state else "NOT-repeat"
        return [state_str,]

    @property
    def ids(self):
        return self._state2id.values()
