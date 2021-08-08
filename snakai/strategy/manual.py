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
    def gen_next_action(self, _, exe):
        """gen next action. 
        here we don't need state.
        """
        ui = exe.ui
        frame_seconds = exe.frame_seconds

        key_waiting_timeout_ms = int(frame_seconds * 1000)
        key = ui.getch(key_waiting_timeout_ms)

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