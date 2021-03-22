# -*- coding: utf-8 -*-
"""snake executor strategy based on Q-Learning
"""
import enum
import argparse
import typing

import numpy as np

from .qtable import QTable
from ..base import Action, Strategy
from ... import snake_state_machine as ssm


class QLearningStrategy(Strategy):
    """Q-Learning strategy
    it both has training & infer api.
    """
    def __init_(self, 
            is_infer: bool, 
            train_args: typing.Optional[argparse.Namespace], 
            infer_args: typing.Optional[argparse.Namespace]):
        """init strategy.
        """
        if is_infer:
            with open(infer_args.model_path, mode="b") as mf:
                self._qtable = pickle.load(mf)
        else:
            self._qtable = QTable(win_width=train_args.win_width, win_height=train_args.win_height)
            self._learning_rate = train_args.learning_rate
            self._discount = train_args.discount
            # probability of do exploration
            self._exploration_rate = train_args.init_exploration_rate
            self._exploration_decay_delta = self._exploration_rate / train_args.exploration_decay_iterations
            self._rng = np.random.RandomState(train_args.seed)
        self._is_infer = is_infer

    def gen_next_action(self, game_state) -> Action:
        """generating next action according to the game-state
        """
        if not self._is_infer and self._rng.rand() < self._exploration_rate:
            # exploration => make a random (but valid) action
            return self._gen_random_action(game_state)
        return self._gen_greedy_action(game_state)

    def _gen_random_action(self, game_state):
        opposite_d = ssm.Direction.get_opposite(game_state.direction)
        candidates = ssm.Direction.get_effective() - {opposite_d,}
        return self._rng.choice(list(candidates))

    def _gen_greedy_action(self, game_state):
        """do exploitation according to QTable
        """

