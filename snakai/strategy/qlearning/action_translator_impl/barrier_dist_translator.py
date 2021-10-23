# -*- coding: utf-8 -*-
"""barrier distance translator
dist -> state enum
"""

import bisect

class BarrierDistTranslator(object):
    """barrier dist translator"""
    def __init__(self):
        self._dist_upperbound = [0, 1]
        self._correspond_states = ["0", "1", "2+"]

    def translate(self, dist: int):
        """translate dist to states"""
        assert dist >= 0, f"dist must >= 0, while got '{dist}'"
        dist_range_idx = bisect.bisect_left(self._dist_upperbound, dist)
        return self._correspond_states[dist_range_idx]

    @property
    def states(self) -> list:
        """get all states"""
        return self._correspond_states