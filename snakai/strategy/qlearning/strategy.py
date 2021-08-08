# -*- coding: utf-8 -*-
"""snake executor strategy based on Q-Learning
"""
import collections
import argparse
import logging
from os import path
import typing
import pickle
import pathlib

import numpy as np

from . import qtable as qtable_module
from . import state_translator
from . import action_translator
from . import reward as reward_module
from .. import base as strategy_base
from .. import register
from ... import snake_state_machine as ssm


logger = logging.getLogger("snakai")

@register("qlearning")
class QLearningStrategy(strategy_base.Strategy):
    """Q-Learning strategy
    it both has training & infer api.
    """
    _Episode = collections.namedtuple("_Episode", ["state_id", "action_id"])

    def __init__(self, 
            is_infer: bool, 
            train_args: typing.Optional[argparse.Namespace], 
            infer_args: typing.Optional[argparse.Namespace]):
        """init strategy.
        """

        if is_infer:
            model_path = infer_args.model_path
            if not model_path:
                model_path = pathlib.Path(__file__).absolute().parent / "output/ql_strategy.pickle"
            with open(model_path, mode="rb") as mf:
                loaded_obj = pickle.load(mf)
                self.__dict__.clear()
                self.__dict__.update(loaded_obj.__dict__)
        else:
            w, h = train_args.win_width, train_args.win_height
            self._state_translator = state_translator.StateTranslator(w, h)
            self._action_translator = action_translator.ActionTranslator()
            self._qtable = qtable_module.QTable(state_size=self._state_translator.size(),
                action_size=self._action_translator.size())

            self._learning_rate = train_args.learning_rate
            self._discount = train_args.discount
            # probability of do exploration
            self._exploration_rate = train_args.init_exploration_rate
            _decay_iter = train_args.exploration_decay_iter
            self._exploration_decay_delta = self._exploration_rate / _decay_iter
            self._rng = np.random.RandomState(train_args.seed)
            self._reward_calc = reward_module.NaiveRewardCalc()

            self._pre_episode = None
            self._cached_cur_state_idx = None
        self._is_infer = is_infer

    def gen_next_action(self, game_state: ssm.SnakeStateMachine, _) -> strategy_base.Action:
        """generating next action according to the game-state
        > will cache the state-id and action. so not thread-safe!
        """
        if self._cached_cur_state_idx is not None:
            # because state is continues, so current state == previour state in updating logic.
            # when updating, it will cache the state-idx to avoid re-calc here.
            state_id = self._cached_cur_state_idx
        else:
            state_id = self._state_translator.state2id(game_state)
        
        if not self._is_infer and self._rng.rand() < self._exploration_rate:
            # exploration => make a random (but valid) action
            action = self._gen_random_action(game_state.direction)
            action_src = "random"
        else:
            action = self._gen_greedy_action(state_id)
            action_src = "greedy"

        action_id = self._action_translator.action2id(action)
        episode = self._Episode(state_id=state_id, action_id=action_id)
        self._pre_episode = episode

        logger.debug("cur state: %s, %s action: %s", _state_id2shorter_str(state_id, self._state_translator), 
            action_src, action)

        return action
    
    def update(self, game_state: ssm.SnakeStateMachine):
        """update QLearning Strategy (QTable)
        Parameters
        =============
        game_state: here should be the new game state, that is
            After taken the previous predicted action.
        """
        reward = self._reward_calc.calc(game_state)
        if game_state.is_state_ok():
            # game still running
            new_state_idx = self._state_translator.state2id(game_state)

            action_id = self._qtable.get_action_of_max_score(new_state_idx)
            max_score = self._qtable.get_score(new_state_idx, action_id)
            q_target = reward + self._discount * max_score
        else:
            new_state_idx = None
            # ended (ignore pause condition)
            q_target = reward
        q_predict = self._qtable.get_score(**self._pre_episode._asdict())
        new_score = q_predict + self._learning_rate * (q_target - q_predict)
        self._qtable.update_score(**self._pre_episode._asdict(), score=new_score)
        logger.debug("after action, reward=%.2f, state new-score = %.2f, table filling ratio: %.1f%%", 
            reward, new_score, self._qtable.table_filling_ratio() * 100)
        self._cached_cur_state_idx = new_state_idx

    def clear4next(self, _):
        """clear inner state and ready for next new strategy. 
        here clear inner status
        """
        self._pre_episode = None
        self._cached_cur_state_idx = None
        self._reward_calc.clear4next()
        if self._exploration_rate > 0:
            self._exploration_rate -= self._exploration_decay_delta

    def table_filling_ratio(self):
        """get table filling ratio"""
        return self._qtable.table_filling_ratio()

    def _gen_random_action(self, cur_diction: ssm.Direction) -> strategy_base.Action:
        opposite_d = ssm.DirectionUtil.get_opposite(cur_diction)
        opposite_action = strategy_base.Action.effective_direction2action(opposite_d)
        candidate_action = list(set(self._action_translator.actions()) - {opposite_action,})
        return self._rng.choice(candidate_action)

    def _gen_greedy_action(self, state_idx: int) -> strategy_base.Action:
        """do exploitation according to QTable
        """
        action_idx = self._qtable.get_action_of_max_score(state_idx)
        action = self._action_translator.id2action(action_idx)
        return action


def _state_id2shorter_str(state_id, state_translator):
    inner_state = state_translator.id2inner_state(state_id)
    state_str = ("barrier[up:{s.barrier_up}, down:{s.barrier_down}, left:{s.barrier_left}, right:{s.barrier_right}]"
        "food[x:{s.food_x}, y:{s.food_y}]").format(s=inner_state)
    return state_str