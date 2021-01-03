# -*- coding: utf-8 -*- 
"""manual strategy
"""

import curses

from . import base
from . import register


@register("manual")
class Manual(base.Strategy):
    """manual strategy: accept keyboard strategy
    """
    def __init__(self, curses_ui, wait_key_timeout):
        """
        Parameters
        =============
        curses_ui: CursesSnakeGameUI
        wait_key_timeout: float
            seconds to wait for key.
        """
        self._ui = curses_ui
        # curses.window.timeout use millionseconds instead of seconds.
        self._wait_key_timeout = int(wait_key_timeout * 1000)

    def gen_next_action(self, _):
        """gen next action. 
        here we don't need state.
        """
        key = self._ui.getch(self._wait_key_timeout)
        _A = base.Action
        if key == 27:
            # ESC
            return _A.EXIT
        elif key == ord(' '):
            # Pause / Resume
            return _A.PAUSE_RESUME
        elif key == curses.KEY_LEFT:
            return _A.MOVE_LEFT
        elif key == curses.KEY_RIGHT:
            return _A.MOVE_RIGHT
        elif key == curses.KEY_UP:
            return _A.MOVE_UP
        elif key == curses.KEY_DOWN:
            return _A.MOVE_DOWN
        else:
            # not supporting, set IDLE 
            return _A.IDLE