# -*- coding: utf-8 -*-
"""action translator: Game Action <-> id
"""

from .. import base as strategy_base

class ActionTranslator(object):
    """action translator.
    from inner action (idx) to game action
    """
    _ACTIONS = [
        strategy_base.Action.MOVE_UP,
        strategy_base.Action.MOVE_DOWN,
        strategy_base.Action.MOVE_LEFT,
        strategy_base.Action.MOVE_RIGHT
    ]

    _ACTION2ID = dict((act, idx) for (idx, act) in enumerate(_ACTIONS))

    @classmethod
    def size(cls):
        """get action size
        """
        return len(cls._ACTIONS)

    @classmethod
    def id2action(cls, aid) -> strategy_base.Action:
        """inner action id to action"""
        return cls._ACTIONS[aid]

    @classmethod
    def action2id(cls, action) -> int:
        """action to id"""
        return cls._ACTION2ID[action]

    @classmethod
    def actions(cls):
        """get all actions"""
        return cls._ACTIONS