# -*- coding: utf-8 -*-
"""state translator
from GameState to index
"""
import collections
import logging

import numpy as np

from ... import snake_state_machine as ssm
from ... import snake_state_machine_util as ssm_util


logger = logging.getLogger("snakai")


class StateTranslator(object):
    """defines State translator.
    from a game-state to QLearning state (index represented)
    """
    _InnerState = collections.namedtuple("_InnerState", ["barrier_up", "barrier_down", 
            "barrier_left", "barrier_right", "food_x", "food_y"])

    def __init__(self, win_width, win_height):
        self._w = win_width
        self._h = win_height
        # max-distance should be `x + 1`. 
        # because we should considering the extra borders!
        # see, it width = 5, then the left border idx = 0, right border idx = 6, the max-dist = 6
        self._x_encoder = _DistanceDiscretizer(win_width + 1)
        self._y_encoder = _DistanceDiscretizer(win_height + 1)
        self._inner_state2id = self._build_state2id()
        self._id2inner_state = {v: k for (k, v) in self._inner_state2id.items()}

    def state2id(self, game_state: ssm.SnakeStateMachine) -> int:
        """from game-state to index (0 based)
        1. game-state -> inner state
        2. inner state -> id
        """
        inner_state = self._game_state2inner_state(game_state)
        return self._inner_state2id[inner_state]

    def id2inner_state(self, state_id) -> 'StateTranslator._InnerState':
        """index to inner state (can't translated to original state)"""
        return self._id2inner_state[state_id]

    def size(self):
        """get size
        """
        return len(self._inner_state2id)

    def __getstate__(self):
        """for pickle
        """
        state = {
            "_x_encoder": self._x_encoder,
            "_y_encoder": self._y_encoder
        }

        state_id_value_pairs = [(_s._asdict(), _id) for (_s, _id) in self._inner_state2id.items()]
        state["state_id_pairs"] = state_id_value_pairs
        return state

    def __setstate__(self, state):
        """for pickle"""
        state2id = {}
        id2state = {}
        for (s_dict, s_id) in state["state_id_pairs"]:
            inner_state = self._InnerState(**s_dict)
            state2id[inner_state] = s_id
            id2state[s_id] = inner_state
        del state["state_id_pairs"]
        self.__dict__.update(**state, _inner_state2id=state2id, _id2inner_state=id2state)

    def _build_state2id(self):
        """
        state has 2 mainly aspect
        1. snake head to barrier distance
        2. snake head to food distance
        state encode following order 
            (barrier-up, barrier-down, barrier-left, barrier-right, food-x, food-y)

        * for barrier distance
          we calc the head to the up/down/left/right barrier distance
          distance = abs(head.x - barrier.x) (left/right), value in range [0, width - 1]
                     abs(head.y - barrier.y) (up/down), value in range [0, height - 1]

        * for food distance
          distance like barrier, but should consider the direction.
          so don't use abs.
          x-distance = head.x - food.x, value in range [-(width - 1), width - 1]
          y-distance = head.y - food.y, value in range [-(height - 1), height - 1]
        """
        # because distance may be too large to represented as states
        # we pre-compress it using descretize.

        discrete_x_ids = self._x_encoder.ids()
        discrete_y_ids = self._y_encoder.ids()
        # in fact, zero distance's state is 0. but we do a more general operation.
        discrete_x_ids_except_zero = [_i for _i in discrete_x_ids 
            if _i != self._x_encoder.zero_dist_id()]
        discrete_y_ids_excpet_zero = [_i for _i in discrete_y_ids
            if _i != self._y_encoder.zero_dist_id()]

        x_barrier_states = discrete_x_ids
        y_barrier_states = discrete_y_ids
        # because x-food has positive/negative distance, but discreter only has positive
        # so we make a extra negative state for non-zero distance states
        # here we just use `-v` (i.e. `-_i`) to represetes a negative state.
        x_food_states = discrete_x_ids + [-_i for _i in discrete_x_ids_except_zero]
        y_food_states = discrete_y_ids + [-_i for _i in discrete_y_ids_excpet_zero]
        
        iter_state_schemas = [
            y_barrier_states,  # up
            y_barrier_states,  # down
            x_barrier_states,  # left
            x_barrier_states,  # right
            x_food_states,  # x row
            y_food_states  # y row
        ]
        
        # qstate(InnerState) -> index
        _state2idx = {}

        # we just make a brute-force composition. it can't has this following
        # so-many states in reality 
        # -> such as, if barrier-up has max distance, then barrier-down can't has max dist.
        #    but here brute-force composition don't sondier this condition.
        def _recursive_build_state(current_state, iter_state_schema_idx):
            if iter_state_schema_idx >= len(iter_state_schemas):
                state_tuple = self._InnerState(*current_state)
                assert state_tuple not in _state2idx, f"{state_tuple} already in state2idx"
                _state2idx[state_tuple] = len(_state2idx)
                return
            cur_direction_states = iter_state_schemas[iter_state_schema_idx]
            for s in cur_direction_states:
                current_state.append(s)
                _recursive_build_state(current_state, iter_state_schema_idx + 1)
                current_state.pop()

        _recursive_build_state([], 0)
        logger.debug("build QStateTranslater, full state size = %d", len(_state2idx))
        return _state2idx

    def _game_state2inner_state(self, game_state: ssm.SnakeStateMachine):
        """
        game_state: snake_state_machine.SnakeStateMachine
        inner_state: _InnerState
        """
        def _encode_with_sign(encoder, dist):
            abs_id = encoder.dist2id(abs(dist))
            return np.sign(dist) * abs_id

        # no-matter snake whether fail, we just encode the state
        distance_calc = ssm_util.DistanceCalc(game_state)
        up_dist = distance_calc.barrier_up_dist()
        down_dist = distance_calc.barrier_down_dist()
        left_dist = distance_calc.barrier_left_dist()
        right_dist = distance_calc.barrier_right_dist()
        (food_x_with_sign, food_y_with_sign) = distance_calc.food_dist_with_sign()

        # logger.debug("state = %s, up %d, down %d, left %d, right %d", game_state, 
        #     up_dist, down_dist, left_dist, right_dist)

        return self._InnerState(
            barrier_up=self._y_encoder.dist2id(up_dist),
            barrier_down=self._y_encoder.dist2id(down_dist),
            barrier_left=self._x_encoder.dist2id(left_dist),
            barrier_right=self._x_encoder.dist2id(right_dist), 
            food_x=_encode_with_sign(self._x_encoder, food_x_with_sign),
            food_y=_encode_with_sign(self._y_encoder, food_y_with_sign))


class _DistanceDiscretizer(object):
    """continues distance -> discretized value
    """
    _MAX_ID = 4

    def __init__(self, max_distance):
        """given max distance
        """
        assert max_distance > 0
        self._max_dist = max_distance
        self._dist2id = self._make_dist2id_map(max_distance)
        self._ids = list(set(self._dist2id))

    def dist2id(self, dist):
        """distance to decretized id
        """
        # here we make a compatibility for bigger dist.
        # because we may train in small graph and infer in big graph
        if dist > self._max_dist:
            logger.warning("got bigger distance: %d, just set to max-distance [%d] as default", dist, self._max_dist)
            dist = self._max_dist
        return self._dist2id[dist]

    def ids(self):
        """get all dicretized id
        """
        return self._ids

    def zero_dist_id(self):
        """get zero-distance id"""
        return self._dist2id[0]

    @classmethod
    def _make_dist2id_map(cls, max_distance):
        # distance in range [0, max_distance], has elements max_distance + 1
        _m = np.zeros([max_distance + 1,], dtype=np.int32)
        # we assine the map like:
        # 0 1 2 2 3 3 3 4 4 4 4 5 ... until the _MAX_ID
        current_sidx = 1
        current_width = 1
        while current_sidx <= max_distance:
            end_idx = current_sidx + current_width
            _m[current_sidx: end_idx] = min(current_width, cls._MAX_ID)
            current_sidx = end_idx
            current_width += 1
        return _m
