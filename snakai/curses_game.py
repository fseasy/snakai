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
    FOOD_CH = "*"
    SNAKE_CH = "#"

    WIDTH = 60
    HEIGHT = 20

    # name to interval seconds
    SPEED = {
        "normal": 0.15,
        "fast": 0.3,
        "slow": 0.5
    }
    # use the same direction key to speed up snake running
    SPEED_UP_RATIO = 5

    def __init__(self, speed="normal"):
        self._frame_time = self.SPEED[speed]
        self._game_state = snake_state_machine.SnakeStateMachine(self.WIDTH, self.HEIGHT)
        self._ui = CursesSnakeGameUI(self.WIDTH, self.HEIGHT)

    def run(self, strategy):
        """run game
        strategy: strategy.Strategy
        """
        with self._ui.active_env():
            self._ui.init_window()
            
            self._game_state.new_state()
            self._draw_init_state()
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

    def _draw_init_state(self):
        # food
        self._ui.draw_point(self._game_state.food, self.FOOD_CH)
        # body
        for p in self._game_state.snake:
            self._ui.draw_point(p, self.SNAKE_CH)
        # score
        self._ui.set_score(self._game_state.score)

    def _update_state_and_draw(self, direction):
        """given a new direction, update the game-state and draw 
        """
        gs = self._game_state
        ui = self._ui
        ui.curses_log(f"got direction: {direction}")
        # cache previous state
        before_update_score = gs.score
        before_update_tail = gs.snake[-1]
        # update state
        gs.update_state(direction)
        if not gs.is_state_ok():
            # direction cause state failed.
            return False
        # draw ui
        new_head = gs.snake[0]
        ui.draw_point(new_head, self.SNAKE_CH)
        new_score = gs.score
        has_eat_food = new_score > before_update_score
        if not has_eat_food:
            # => food hadn't been eatten => erase tail
            ui.erase_point(before_update_tail)
        else:
            # => new food(no need to erase previous food), new score
            ui.draw_point(gs.food, self.FOOD_CH)
            ui.set_score(new_score)
        return True

    def _print_result(self):
        # check result and echo
        if self._game_state.is_end_with_successed():
            print("Congratulations! You Succeed! Score = {}".format(self._game_state.score))
        else:
            print("Game Over. Score = {} in steps {}".format(self._game_state.score, self._game_state.steps))

    def _exe_game(self, strategy):
        """execute game (while loop)
        """
        _A = base_strategy.Action
        _D = snake_state_machine.Direction
        action2direction = {
            _A.MOVE_LEFT: _D.LEFT,
            _A.MOVE_RIGHT: _D.RIGHT,
            _A.MOVE_DOWN: _D.DOWN,
            _A.MOVE_UP: _D.UP,
            _A.IDLE: _D.NONE
        }
        
        is_paused = False

        while True:
            direction = _D.NONE
            # action and direction
            with keep_time(self.frame_time / self.SPEED_UP_RATIO):
                action = strategy.gen_next_action(self._game_state)

            if action == _A.EXIT:
                break
            elif action == _A.PAUSE_RESUME:
                is_paused = not is_paused
            elif action in action2direction:
                direction = action2direction[action]
            
            if is_paused:
                self._ui.curses_log("Paused. use [SPACE] to Resume.")
                continue

            # update
            is_ok = self._update_state_and_draw(direction)
            if not is_ok:
                break


class CursesSnakeGameUI(object):
    """ui for curses sname game
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
        win = curses.newwin(self._h + 2, self._w + 2, 0, 0)
        # bind the win
        self._win = win

        win.keypad(1)
        win.border(0)
        win.nodelay(1)
        win.border(0)
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