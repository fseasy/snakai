# -*- coding: utf-8 -*-
""" Q-Learning table
it includes state, action, state2action-value-sheet(QTable)
"""
import numpy as np


class QTable(object):
    """Q table
    Q table here could be viewed as matrix, represents state -> action value sheet.
        row is the states
        col is the action.
        value is the action score.  

        state mapping or action mapping is controlled in outter.
        QTable only has index view.
    """
    def __init__(self, state_size, action_size):
        """init q table
        """
        self._table = np.zeros((state_size, action_size), dtype=np.float32)
        self._debug_table_update_cnt = np.zeros((state_size, action_size), dtype=np.int32)

    def get_action_of_max_score(self, state_id: int) -> int:
        """get action with max score of current game-state
        """ 
        action_idx = self._table[state_id].argmax(axis=0)
        return action_idx

    def get_score(self, state_id: int, action_id: int):
        """get score"""
        return self._table[state_id, action_id]

    def update_score(self, state_id: int, action_id: int, score: float):
        """update score"""
        self._table[state_id, action_id] = score
        self._debug_table_update_cnt[state_id, action_id] += 1

    def table_filling_ratio(self):
        """get table filling ratio"""
        return np.count_nonzero(self._debug_table_update_cnt) / self._debug_table_update_cnt.size