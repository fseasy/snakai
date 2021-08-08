# -*- coding: utf-8 -*-
"""reward calc
"""
import logging

from ... import snake_state_machine as ssm


logger = logging.getLogger("snakai")


class NaiveRewardCalc(object):
    """calculator for reward in naive
    """
    def __init__(self):
        self._env_prev_score = 0.
        self._step_after_last_gain = 0

    def calc(self, game_state: ssm.SnakeStateMachine) -> float:
        """get reward
        """
        reward = self._calc_reward(game_state)
        return reward

    def clear4next(self):
        """clear inner state for next updating"""
        self._env_prev_score = 0.
        self._step_after_last_gain = 0

    def _calc_reward(self, game_state):
        if game_state.is_fail():
            return -50.
        elif game_state.is_success():
            return 100.
        env_score = game_state.score
        if env_score > self._env_prev_score:
            self._env_prev_score = env_score
            self._step_after_last_gain = 0
            return 50.
        else:
            self._step_after_last_gain += 1
            _ref_len = game_state.state_width + game_state.state_height
            times = self._step_after_last_gain // _ref_len
            reward = - 1 / 1000 * (10 ** times)
            return reward