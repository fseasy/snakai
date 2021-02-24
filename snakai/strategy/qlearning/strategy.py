# -*- coding: utf-8 -*-
"""snake executor strategy based on Q-Learning
"""
import enum
import argparse

from ... import snake_state_machine as ssm
from ..base import Action, Strategy


class QLearningStrategy(Strategy):
    """Q-Learning strategy
    it both has training & infer api.
    """
    def __init_(self, is_infer: bool, train_args: argparse.Namespace):
        """init strategy.
        """
        self.qstate = QState()
        if is_infer:
            


    def gen_next_action(self, game_state) -> Action:
        """generating next action according to the game-state
        """
        pass


