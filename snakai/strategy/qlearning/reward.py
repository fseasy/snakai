# -*- coding: utf-8 -*-
"""reward calc
"""

from ... import snake_state_machine as ssm

class NaiveRewardCalc(object):
    """calculator for reward in naive
    """
    def __init__(self):
        self._env_prev_score = 0.
        self._episode_after_last_gain = 0

    def __call__(self, game_state: ssm.SnakeStateMachine) -> float:
        """get reward
        """
        if game_state.is_fail():
            return -40.
        elif game_state.is_success():
            return 100.
        env_score = game_state.score
        if env_score > self._env_prev_score:
            self._env_prev_score = env_score
            self._episode_after_last_gain = 0
            return 2.
        else:
            self._episode_after_last_gain += 1
            reward = - self._episode_after_last_gain / 100.
            return reward
