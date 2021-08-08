# -*- coding: utf-8 -*-
"""curses ui impl for Snake
"""
import contextlib
import curses
import time


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
        stdscr = curses.initscr()
        try:
            stdscr.keypad(True)
            curses.noecho()
            curses.cbreak()
            # disable cursor display
            curses.curs_set(0)

            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_YELLOW, -1)
            curses.init_pair(2, curses.COLOR_CYAN, -1)

            yield stdscr
        except:
            raise
        finally:
            # release, or it will break the terminal
            stdscr.keypad(False)
            curses.nocbreak()
            curses.echo()
            curses.endwin()

    def init_window(self):
        """init curses env and 
        """
        # both height, width has extra border line. so following point should also has 1 offset
        win = curses.newwin(self._h + 2, self._w + 2, 0, 0)

        win.keypad(True)
        # explicitly set the border char (Ubuntu Gnome ternimal may render `wide-char` for default h value)
        win.box("|", "|")
        win.nodelay(True)

        # bind the win and render others
        self._win = win
        self.set_score(0)
        self.set_title("SNAKAI")

    def getch(self, timeout):
        """get char from standard input
        """
        self._win.timeout(timeout)
        return self._win.getch()

    def set_score(self, score):
        """update snake game score
        """
        self._win.addstr(0, 2, f'Score: {score} ', curses.color_pair(2))

    def set_title(self, title):
        """set title"""
        tlen = len(title)
        left_pad = (self._w - tlen) // 2
        self._win.addstr(0, left_pad, title, curses.color_pair(1))
    
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
