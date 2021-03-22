# -*- coding: utf-8 -*-
""" Q-Learning table
it includes state, action, state2action-value-sheet(QTable)
"""
import collections

import numpy as np


class QTable(object):
    """Q table
    """
    def __init__(self, win_width, win_height):
        """init q table
        """
        self._state_translator = QStateTranslator(win_width, win_height)
        self._action_translator = ActionTranslator()
        _state_sz = self._state_translator.size()
        _action_sz = self._action_translator.size()
        self._raw_table = np.zeros(
            (_state_sz, _action_sz), 0., dtype=np.float32)
        self._rng = np.random.RandomState(1234)

    def get_max_action(self, game_state):
        """get max action of current game-state
        """ 
        state_idx = self._state_translator.state2id(game_state)


class QStateTranslator(object):
    """defines QState translator.
    from a game-state to QLearning state (index represented)
    """
    _InnerState = collections.namedtuple("_InnerState", ["barrier_up", "barrier_down", 
            "barrier_left", "barrier_right", "food_x", "food_y"])

    def __init__(self, win_width, win_height):
        self._w = win_width
        self._h = win_height
        self._x_encoder = _DistanceDiscretizer(win_width)
        self._y_encoder = _DistanceDiscretizer(win_height)
        self._inner_state2id = self._build_state2id()

    def state2id(self, game_state):
        """from game-state to index
        1. game-state -> inner state
        2. inner state -> idx
        """
        ## 1. game-state -> inner state
        # 
        ## 2. inner-state -> idx

    def size():
        """get size
        """
        return len(self._inner_state2id)

    def _build_state2id(self):
        """
        state has 2 mainly aspect
        1. snake head to barrier distance
        2. snake head to food distance
        state encode following order 
            (barrier-up, barrier-down, barrier-left, barrier-right, food-x, food-y)
        """
        x_valid_id_sz = self._x_encoder.size()
        y_valid_id_sz = self._y_encoder.size()
        # * for barrier distance
        # besides the valid distance,
        # snake has invalid distance for direction of opposite
        # e.g. snake head towards right, then for left, it is invalid direction.
        # this condition should be distinguished from valid distance 0
        # in 1 state, only 1 direction can be invalid direction.
        # this means, the full barrier state size should be
        # x-vald-size ^ 2 * y-valid-size * 2
        # + 2 * x-valid-size * y-valid-size ^ 2   (that is:  y * y *x * 1 + y * y * 1 * x))
        # + 2 * x-valid-size ^ 2 * y-valid-size
        # * for food distance
        # it has positive and negative. say: -max-id ... 0 ... max-id = 2 * max-id - 1
        # full food states num = x-states * y-states
        _m = {}
        _invalid_state_id = -1
        x_barrier_states = [_invalid_state_id, ] + list(range(x_valid_id_sz))
        y_barrier_states = [_invalid_state_id, ] + list(range(y_valid_id_sz))
        x_food_states = [
            x for x in range(-x_valid_id_sz + 1, 0)] + list(range(x_valid_id_sz))
        y_food_states = [
            y for y in range(-y_valid_id_sz + 1, 0)] + list(range(y_valid_id_sz))
        iter_state_schemas = [
            y_barrier_states,  # up
            y_barrier_states,  # down
            x_barrier_states,  # left
            x_barrier_states,  # right
            x_food_states,  # x row
            y_food_states  # y row
        ]

        def _recursive_build_state(current_state, iter_state_schema_idx):
            if iter_state_schema_idx >= len(iter_state_schemas):
                state_tuple = self._InnerState(*current_state)
                _m[state_tuple] = len(_m)
                return
            cur_direction_states = iter_state_schames[iter_state_schema_idx]
            # ensure only 1 invlaid-id in 1 full state
            if _invalid_state_id in current_state:
                cur_direction_states = [_s for _s in cur_direction_states
                                        if _s != _invalid_state_id]
            for s in cur_direction_states:
                current_state.append(s)
                recursive_build_state(current_state, iter_state_schema_idx + 1)
                current_state.pop()

        _recursive_build_state([], 0)
        assert len(_m) = ((x_valid_id_sz ** 2 * y_valid_id_sz ** 2
                           + 2 * x_valid_id_sz ** 2 * y_valid_id_sz
                           + 2 * x_valid_id_sz * y_valid_id_sz ** 2)
                          * (2 * x_valid_id_sz - 1)
                          * (2 * y_valid_id_sz - 1))
        return _m

    def _game_state2inner_state(self, game_state):
        """
        game_state: snake_state_machine.SnakeStateMachine
        inner_state: _InnerState
        """
        # TODO here: need calc to food distance.
        if game_state.is_fail():
            return 


class ActionTranslator(object):
    """action translator.
    from inner action (idx) to game action
    """
    _SZ = 4

    @classmethod
    def size(cls):
        """get action size
        """
        return cls._SZ


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

    def dist2id(self, dist):
        assert 0 <= dist <= self._max_dist
        return self._dist2id[dist]

    def size(self):
        """get discretized id size
        """
        return self._dist2id[-1] + 1

    @classmethod
    def _make_dist2id_map(cls, max_distance):
        # distace in range [0, max_distance], has elements max_distance + 1
        _m = numpy.zeros(max_distance + 1, dtype=np.int32)
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
