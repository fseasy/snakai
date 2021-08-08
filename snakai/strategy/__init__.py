# -*- coding: utf-8 -*-
"""strategy inialization.
"""

_name2startegy_cls = {}

def register(name):
    if name in _name2startegy_cls:
        raise ValueError(f"dup-register. strategy [{name}] has already exists!")

    def _decorator_fn(cls):
        _name2startegy_cls[name] = cls
        return cls

    return _decorator_fn


def get_names():
    """get strategy names
    """
    return list(_name2startegy_cls.keys())


def get_strategy_cls(name):
    """name 2 strategy cls
    """
    return _name2startegy_cls[name]


def init_strategy(name, args):
    """init strategy
    """
    cls = get_strategy_cls(name)
    if name == "manual":
        return cls()
    elif name == "rule_based":
        return cls()
    elif name == "qlearning":
        return cls(is_infer=True, infer_args=args, train_args=None)
    raise ValueError(f"strategy class {name} has not proper initialization")


from . import manual
from . import rule_based
from . import qlearning