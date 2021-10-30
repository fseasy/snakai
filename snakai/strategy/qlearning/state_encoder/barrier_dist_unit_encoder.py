# -*- coding: utf-8 -*-
"""barrier distance encoder
dist -> state enum
"""

import bisect

from .encoder_base import EncoderBase

class BarrierDistUnitEncoder(EncoderBase):
    """barrier dist encoder"""
    def __init__(self):
        self._dist_upperbound = [0, 1]
        self._correspond_states = ["0", "1", "2+"]
        self._state2id = {_s: _i for (_i, _s) in enumerate(self._correspond_states)}

    def encode(self, dist: int) -> int:
        """encode dist to states"""
        assert dist >= 0, f"dist must >= 0, while got '{dist}'"
        dist_range_idx = bisect.bisect_left(self._dist_upperbound, dist)
        s = self._correspond_states[dist_range_idx]
        return self._state2id[s]

    def readable_state(self, state_id) -> list:
        return [self._correspond_states[state_id]]

    @property
    def ids(self) -> list:
        return self._state2id.values()