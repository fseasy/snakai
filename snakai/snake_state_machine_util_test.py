# -*- coding: utf8 -*-
"""test (pytest)
"""
import collections

from . import snake_state_machine as ssm
from . import snake_state_machine_util as ssm_util

def test_distance_calc():
    state = ssm.SnakeStateMachine(width=20, height=23)
    _P = ssm.Point
    # 
    #  * h
    #  *
    #  ....
    #  f
    state.snake = collections.deque([
        _P(3, 4), _P(2, 4), _P(2, 3)
    ])
    state.food = _P(2, 9)
    
    calc = ssm_util.DistanceCalc(state)
    assert calc.barrier_up_dist() == 4
    assert calc.barrier_down_dist() == 23 - 4
    assert calc.barrier_left_dist() == 1
    assert calc.barrier_right_dist() == 20 - 3
    assert calc.food_dist_with_sign() == (1, -5)
    #
    #    *  * *
    #    * h  *
    #      *   *
    #     f
    # for easily, not valid body
    state.snake = collections.deque([
        _P(10, 10), 
        # x axis diff
        _P(9, 10), _P(1, 10), _P(13, 10), _P(2, 10),
        # y axis diff
        _P(10, 11), _P(10, 13), _P(10, 0), _P(10, 2)
    ])
    state.food = _P(0, 20)

    calc = ssm_util.DistanceCalc(state)
    assert calc.barrier_up_dist() == 8
    assert calc.barrier_down_dist() == 1
    assert calc.barrier_left_dist() == 1
    assert calc.barrier_right_dist() == 3
    assert calc.food_dist_with_sign() == (10, -10)

    state.snake = collections.deque([_P(1, 1), _P(1, 1)])
    calc = ssm_util.DistanceCalc(state)
    assert calc.barrier_up_dist() == calc.barrier_down_dist() == 0
    assert calc.barrier_left_dist() == calc.barrier_right_dist() == 0