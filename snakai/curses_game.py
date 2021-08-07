# -*- coding: utf-8 -*-
"""curses based snake game.
guided by https://gist.github.com/sanchitgangwar/2158089
"""

import contextlib
import curses
import time

from . import snake_state_machine
from .strategy import base as base_strategy


class CursesSnakeGameExe(object):
    """Curses based snake executor
    """
    # name to interval seconds
    SPEED = {
        "normal": 0.15,
        "fast": 0.3,
        "slow": 0.5
    }
    # use the same direction key to speed up snake running
    SPEED_UP_RATIO = 5

    def __init__(self, win_width=60, win_height=20, speed="normal"):
        self._frame_time = self.SPEED[speed]
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
    def curses_ui(self):
        """return curses ui
        """
        return self._ui

    @property
    def frame_time(self):
        """get game frame time
        """
        return self._frame_time

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
            with keep_time(self.frame_time / self.SPEED_UP_RATIO):
                action = strategy.gen_next_action(self._game_state)

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


class SnakeStateRender(object):
    """game state render under the UI framework
    """
    FOOD_CH = "*"
    SNAKE_CH = "#"

    def __init__(self, ui_framework: 'SnakeUIFramework'):
        self._ui = ui_framework
        self._previours_score = None
        self._previours_tail = None

    def render_init_state(self, game_state):
        """render initial game state"""
        # food
        self._ui.draw_point(game_state.food, self.FOOD_CH)
        # body
        for p in game_state.snake:
            self._ui.draw_point(p, self.SNAKE_CH)
        # score
        self._ui.set_score(game_state.score)
        # record state key information for updating render
        self._previours_score = game_state.score
        self._previours_tail = game_state.snake[-1]

    def render_updated_state(self, game_state):
        """render updated state"""
        gs = game_state
        ui = self._ui
        # draw ui
        new_head = gs.snake[0]
        ui.draw_point(new_head, self.SNAKE_CH)
        new_score = gs.score
        has_eat_food = new_score > self._previours_score
        if not has_eat_food:
            # => food hadn't been eatten => erase tail
            ui.erase_point(self._previours_tail)
        else:
            # => new food(no need to erase previous food), new score
            ui.draw_point(gs.food, self.FOOD_CH)
            ui.set_score(new_score)
        # update key information
        self._previours_score = new_score
        self._previours_tail = game_state.snake[-1]


class SnakeUIFramework(object):
    """ui framework for curses sname game
    a lower api for drawing.
    """
    def __init__(self, width, height):
        self._w = width
        self._h = height
        self._win = None

    @contextlib.contextmanager
    def active_env(self):
        """curses need init and properly exit
        """
        stdcsr = curses.initscr()
        stdcsr.keypad(1)
        curses.noecho()
        curses.curs_set(0)
        try:
            yield stdcsr
        except:
            raise
        finally:
            # release, or it will break the terminal
            stdcsr.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()

    def init_window(self):
        """init curses env and 
        """
        # both height, width has extra border line. so following point should also has 1 offset
        win = curses.newwin(self._h + 2, self._w + 2, 0, 0)
        # bind the win
        self._win = win

        win.keypad(1)
        win.border(0)
        win.nodelay(1)
        win.addstr(0, 27, ' SNAKE ')

        self.set_score(0)

    def getch(self, timeout):
        """get char from standard input
        """
        self._win.timeout(timeout)
        return self._win.getch()

    def set_score(self, score):
        """update snake game score
        """
        self._win.addstr(0, 2, f'Score : {score} ')
    
    def draw_point(self, point, c):
        """draw character `c` in point
        """
        # plus 1 offset for boder line
        self._win.addch(point.y + 1, point.x + 1, c)        

    def erase_point(self, point):
        """erase curses point => use space to draw the target point
        """
        self.draw_point(point, " ")

    def curses_log(self, s):
        """curses log
        """
        self._win.addstr(self._h + 1, 0, s)

    def refresh(self):
        """curses need refresh, so that it can draw!
        `getch` implictly call `refresh`
        https://stackoverflow.com/questions/19748685/curses-library-why-does-getch-clear-my-screen
        """
        self._win.refresh()
        

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
