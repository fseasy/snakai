# -*- coding: utf-8 -*-
""" Q-Learning table
it includes state, action, state2action-value-sheet(QTable)
"""

class QState(object):
    """defines QState.
    from a game-state to QLearning state (index represented)
    """
    def __init__(self, win_width, win_height):
        self._w = win_width
        self._h = win_height
