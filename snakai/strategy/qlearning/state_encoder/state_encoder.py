# -*- coding: utf-8 -*-
"""state encoder
from GameState to index
"""
import logging
import itertools

from snakai import snake_state_machine as ssm
from snakai import snake_state_machine_util as ssm_util

from . import common
from .dist_encoder import DistEncoder
from .direction_encoder import DirectionEncoder

logger = logging.getLogger("snakai")


class StateEncoder(object):
    """defines State encoder.
    from a game-state to QLearning state (index represented)
    """
    def __init__(self):
        self._encoders = [DistEncoder(), DirectionEncoder()]
        self._id2state = common.build_all_states(self._encoders)
        self._state2id = {_s: _i for (_i, _s) in enumerate(self._id2state)}

    def encode(self, game_state: ssm.SnakeStateMachine) -> int:
        """from game-state to index (0 based)
        1. game-state -> inner state
        2. inner state -> id
        """
        state = [e.encode(game_state) for e in self._encoders]
        return self._state2id[tuple(state)]

    def readable_state(self, state_id) -> list:
        state = self._id2state[state_id]
        decodes = [e.readable_state(s) for (e, s) in zip(self._encoders, state)]
        return itertools.chain(*decodes)

    @property
    def states(self):
        return self._id2state

    @property
    def size(self):
        """get size
        """
        return len(self._id2state)
