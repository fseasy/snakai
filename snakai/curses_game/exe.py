# -*- coding: utf-8 -*-
"""Game executor.
guided by https://gist.github.com/sanchitgangwar/2158089
"""
import contextlib
import time
import enum

from .ui import SnakeUIFramework, SnakeStateRender
from .. import snake_state_machine
from ..strategy import base as base_strategy


class CursesSnakeGameExe(object):
    """Curses based snake executor
    """
    # use the same direction key to speed up snake running
    SPEED_UP_RATIO = 5

    def __init__(self, win_width=60, win_height=20, speed="normal"):
        self._frame_seconds = self._speed2frame_seconds(speed)
        self._game_state = snake_state_machine.SnakeStateMachine(win_width, win_height)
        self._ui = SnakeUIFramework(win_width, win_height)
        self._state_render = SnakeStateRender(self._ui)

    def run(self, strategy):
        """run game
        strategy: strategy.Strategy
        """
        with self._ui.active_env():
            self._ui.init_window()
            # init
            self._game_state.new_state()
            self._state_render.render_init_state(self._game_state)
            # exe continues
            self._exe_game(strategy)

        self._print_result()

    @property
    def ui(self):
        """return curses ui
        """
        return self._ui

    @property
    def frame_seconds(self):
        """get game frame seconds
        """
        return self._frame_seconds

    def _exe_game(self, strategy):
        """execute game (while loop)
        """
        _A = base_strategy.Action
        _D = snake_state_machine.Direction

        is_paused = False
        while True:
            # need refresh to display the latest view
            self._ui.refresh()
            
            # receive next action
            with keep_time(self.frame_seconds / self.SPEED_UP_RATIO):
                action = strategy.gen_next_action(self._game_state, self)

            self._ui.curses_log(f"get action = {action}")

            if action == _A.EXIT:
                break
            elif action == _A.PAUSE_RESUME:
                is_paused = not is_paused
                direction = _D.NONE
            elif action == _A.IDLE:
                direction = _D.NONE
            else:
                direction = action.to_direction()
            
            if is_paused:
                self._ui.curses_log("Paused. use [SPACE] to Resume.")
                continue

            # update state
            is_ok = self._game_state.update_state(direction)
            if not is_ok:
                break
            # update ui render
            self._state_render.render_updated_state(self._game_state)

    def _print_result(self):
        # check result and echo
        if self._game_state.is_success():
            print("Congratulations! You Succeed! Score = {}".format(self._game_state.score))
        else:
            print("Game Over. Score = {} in steps {}".format(self._game_state.score, self._game_state.steps))

    def _speed2frame_seconds(self, speed_str):
        """speed to frame time"""
        _T = {
            GameSpeed.SLOW: 0.5,
            GameSpeed.NORMAL: 0.15,
            GameSpeed.FAST: 0.1
        }
        return _T[GameSpeed.from_name(speed_str)]


class GameSpeed(enum.Enum):
    """Game Speed"""
    SLOW = enum.auto()
    NORMAL = enum.auto()
    FAST = enum.auto()

    @staticmethod
    def names():
        """get all names"""
        return [e.name for e in GameSpeed]

    @staticmethod
    def from_name(name: str):
        """from name str to enum"""
        return GameSpeed[name.upper()]


@contextlib.contextmanager
def keep_time(target_seconds):
    """keep this code-region running time >= target_seconds
    """
    try:
        stime = time.time()
        yield 
        etime = time.time()
        cost_time = etime - stime
        left_time = target_seconds - cost_time
        if left_time > 0.:
            time.sleep(left_time)
    except:
        raise
    finally:
        pass
