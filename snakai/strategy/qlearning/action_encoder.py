# -*- coding: utf-8 -*-
"""action encoder: Game Action <-> id
"""

from snakai.strategy import base as S

class ActionEncoder(object):
    """action encoder.
    from inner action (idx) to game action
    """
    _ACTIONS = [
        S.Action.MOVE_UP,
        S.Action.MOVE_DOWN,
        S.Action.MOVE_LEFT,
        S.Action.MOVE_RIGHT
    ]

    _ACTION2ID = dict((act, idx) for (idx, act) in enumerate(_ACTIONS))

    @classmethod
    def decode(cls, aid) -> S.Action:
        """inner action id to action"""
        return cls._ACTIONS[aid]

    @classmethod
    def encode(cls, action) -> int:
        """action to id"""
        return cls._ACTION2ID[action]

    @property
    def actions(self):
        """get all actions"""
        return self._ACTIONS

    @property
    def size(self):
        """get action size
        """
        return len(self._ACTIONS)