# -*- coding: utf-8 -*-
"""food distance encoder
"""
import enum

class FoodDistState(enum.Enum):
    ZERO = "0"
    POSITIVE = "positive"
    NEGATIVE = "negative"


class FoodDistUnitEncoder(object):
    """food distance unit encoder"""
    def __init__(self):
        self._states = [s.value for s in FoodDistState]
        self._state2id = {_s:_i for (_i, _s) in enumerate(self._states)}

    def encode(self, dist: int) -> str:
        if dist == 0:
            s = FoodDistState.ZERO.value
        elif dist > 0:
            s = FoodDistState.POSITIVE.value
        else:
            s = FoodDistState.NEGATIVE.value
        return self._state2id[s]

    def readable_state(self, state_id) -> list:
        return [self._states[state_id]]

    @property
    def ids(self):
        return self._state2id.values()


# class _DistanceDiscretizer(object):
#     """continues distance -> discretized value
#     """
#     _MAX_ID = 4

#     def __init__(self, max_distance):
#         """given max distance
#         """
#         assert max_distance > 0
#         self._max_dist = max_distance
#         self._dist2id = self._make_dist2id_map(max_distance)
#         self._ids = list(set(self._dist2id))

#     def dist2id(self, dist):
#         """distance to decretized id
#         """
#         # here we make a compatibility for bigger dist.
#         # because we may train in small graph and infer in big graph
#         if dist > self._max_dist:
#             logger.warning("got bigger distance: %d, just set to max-distance [%d] as default", dist, self._max_dist)
#             dist = self._max_dist
#         return self._dist2id[dist]

#     def ids(self):
#         """get all dicretized id
#         """
#         return self._ids

#     def zero_dist_id(self):
#         """get zero-distance id"""
#         return self._dist2id[0]

#     @classmethod
#     def _make_dist2id_map(cls, max_distance):
#         # distance in range [0, max_distance], has elements max_distance + 1
#         _m = np.zeros([max_distance + 1,], dtype=np.int32)
#         # we assine the map like:
#         # 0 1 2 2 3 3 3 4 4 4 4 5 ... until the _MAX_ID
#         current_sidx = 1
#         current_width = 1
#         while current_sidx <= max_distance:
#             end_idx = current_sidx + current_width
#             _m[current_sidx: end_idx] = min(current_width, cls._MAX_ID)
#             current_sidx = end_idx
#             current_width += 1
#         return _m
