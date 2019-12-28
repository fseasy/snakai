# -*- coding: utf-8 -*-
"""snake game.
guided by https://gist.github.com/sanchitgangwar/2158089
"""

import contextlib
import curses

from snakai.snake import snake_state_machine


class CursesSnakeGame(object):

    def __init__(self):
        self._game_state = snake_state_machine.SnakeStateMachine()
        self._game_state.new_state()
        self._run()

    def _run(self):
        with self._curse_env() as _:
            self._active_game_panel()
        if self._game_state.is_end_with_successed():
            print("Congratulations! You Succeed! Score = {}".format(self._game_state.score))
        else:
            print("Game Over. Score = {} in steps {}".format(
                self._game_state.score, self._game_state.steps))

    def _active_game_panel(self):
        win = curses.newwin(
            self._game_state.window_height + 2, self._game_state.window_width + 2, 
            0, 0)
        win.keypad(1)
        win.border(0)
        win.nodelay(1)
        key2direction_table = {
            curses.KEY_LEFT: snake_state_machine.Direction.LEFT, 
            curses.KEY_RIGHT: snake_state_machine.Direction.RIGHT, 
            curses.KEY_UP: snake_state_machine.Direction.UP, 
            curses.KEY_DOWN: snake_state_machine.Direction.DOWN
        }

        FOOD_CH = "*"
        SNAKE_CH = "#"
        ERASE_CH = " "

        def _curses_log(s):
            win.addstr(self._game_state.window_height + 1, 0, s)

        def _update_score(score):
            win.addstr(0, 2, 'Score : ' + str(score) + ' ')

        def _draw_point(point, ch):
            # plus 1 offset for boder line
            win.addch(point.y + 1, point.x + 1, ch)        

        def _init_window():
            win.border(0)
            win.addstr(0, 27, ' SNAKE ')
            _update_score(self._game_state.score)
            _draw_point(self._game_state.food, FOOD_CH)
            for p in self._game_state.snake:
                _draw_point(p, SNAKE_CH)

        def _update_window(direction):
            current_score = self._game_state.score
            current_snake_tail = self._game_state.snake[-1]

            self._game_state.update_state(direction)
            _curses_log("game state direction: " + str(self._game_state.direction))

            if not self._game_state.is_state_ok():
                return False
            # draw new head
            new_head = self._game_state.snake[0]
            _draw_point(new_head, SNAKE_CH)
            updated_score = self._game_state.score
            if updated_score == current_score:
                # => food hadn't been eatten => erase tail
                _draw_point(current_snake_tail, ERASE_CH)
            else:
                # => new food(no need to erase previous food), new score
                _draw_point(self._game_state.food, FOOD_CH)
                _update_score(updated_score)
            return True

        is_paused = False

        _init_window()
        while True:
            win.timeout(150)
            key = win.getch()
            if key == 27:
                # ESC
                break
            elif key == ord(' '):
                # Pause / Resume
                is_paused = not is_paused
                direction = snake_state_machine.Direction.NONE
            elif key in key2direction_table:
                direction = key2direction_table[key]
                # _curses_log("get direction: " + str(direction))
            else:
                # not supporting, set direction = None
                direction = snake_state_machine.Direction.NONE
            if not is_paused:
                should_continue = _update_window(direction)
                if not should_continue:
                    break
            else:
                _curses_log("Paused. use SPACE to resume.")

    @contextlib.contextmanager
    def _curse_env(self):
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


def main():
    """main program
    """
    CursesSnakeGame()


if __name__ == "__main__":
    main()
