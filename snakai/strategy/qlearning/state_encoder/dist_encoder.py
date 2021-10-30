# -*- coding: utf-8 -*-
"""encoder all distance
"""
import logging

from . import common
from .encoder_base import EncoderBase
from .barrier_dist_unit_encoder import BarrierDistUnitEncoder
from .food_dist_unit_encoder import FoodDistUnitEncoder
from snakai import snake_state_machine as ssm
from snakai import snake_state_machine_util as ssm_util

logger = logging.getLogger("snakai")


class DistEncoder(EncoderBase):
    """dist encoder"""
    def __init__(self):
        self._unit_encoders = [
            # barrier UP, DOWN, LEFT, RIGHT
            BarrierDistUnitEncoder(), BarrierDistUnitEncoder(), BarrierDistUnitEncoder(), BarrierDistUnitEncoder(),
            # food X, Y
            FoodDistUnitEncoder(), FoodDistUnitEncoder()
        ]
        self._id2state = common.build_all_states(self._unit_encoders)
        self._state2id = {_s: _i for (_i, _s) in enumerate(self._id2state)}
    
    def encode(self, game_state: ssm.SnakeStateMachine) -> int:
        """encode dist"""
        distance_calc = ssm_util.DistanceCalc(game_state)
        up_dist = distance_calc.barrier_up_dist()
        down_dist = distance_calc.barrier_down_dist()
        left_dist = distance_calc.barrier_left_dist()
        right_dist = distance_calc.barrier_right_dist()
        (food_x_with_sign, food_y_with_sign) = distance_calc.food_dist_with_sign()

        dists = [
            up_dist, down_dist, left_dist, right_dist,
            food_x_with_sign, food_y_with_sign
        ]

        state = [ue.encode(dist) for (ue, dist) in zip(self._unit_encoders, dists)]
        return self._state2id[tuple(state)]

    def readable_state(self, state_id: int) -> list:
        state = self._id2state[state_id]
        state = [e.readable_state(s)[0] for (e, s) in zip(self._unit_encoders, state)]
        return state

    @property
    def ids(self):
        return self._state2id.values()
