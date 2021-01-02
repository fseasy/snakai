# -*- coding: utf-8 -*-
"""strategy inialization.
"""

_name2startegy_cls = {}

def register(name):
    if name in _name2startegy_cls:
        raise ValueError(f"dup-register. strategy [{name}] has already exists!")

    def _decorator_fn(cls):
        _name2startegy_cls[name] = cls

    return _decorator_fn


def get_names():
    """get strategy names
    """
    return list(_name2startegy_cls.keys())


def get_strategy_cls(name):
    """name 2 strategy cls
    """
    return _name2startegy_cls[name]

from . import manual_strategy


def init_strategy(name, curses_ui, frame_time):
    """init strategy
    """
    cls = get_strategy_cls(name)
    if name == "manual":
        return cls(curses_ui, frame_time)
    raise ValueError(f"strategy class {name} has not proper initialization")