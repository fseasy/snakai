# -*- coding: utf-8 -*-
"""logging setting"""

import logging
import pathlib


def init_logger(name, level=logging.INFO, fpath="log/running.log"):
    """init logger
    """
    # just use the relative dir for easily check log file
    path = pathlib.Path(fpath)
    path.parent.mkdir(exist_ok=True, parents=True)
    
    handler = logging.FileHandler(filename=path, mode="w", encoding="utf-8")
    formatter = logging.Formatter(fmt="{name}:{levelname}/{asctime}/{module}: {message}",
        style="{")
    handler.setFormatter(formatter)
    handler.setLevel(level)
    
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger