# -*- coding: utf-8 -*-
"""snake game.
guided by https://gist.github.com/sanchitgangwar/2158089
"""

import contextlib
import curses
import logging
import random


class SnakeStateMachine(object):
    """snake-state-machine
    only keep inner status, the IO logic should be impl in the other class. 
    """
    class Direction(object):
        """direction"""
        LEFT = 0
        RIGHT = 1
        UP = 2
        DOWN = 3
        UNDEFINED = 4


    class InnerStatus(object):
        """inner status"""
        RUNNING = 0
        END = 1


    def __init__(self):
        """init 
        """
        self.window_height = 20
        self.window_width = 60
        self.snake = None
        self.food = None
        self.score = 0
        self.direction = self.Direction.UNDEFINED
        self.status = self.InnerStatus.END
        self._rng = random.Random(1234)

    def _init_state(self):
        self._init_snake()
        self._init_food()

    def _init_snake(self):
        pass
    
    def _init_food(self):
        pass




class CursesSnakeGame(object):

    def _init__(self):

        with self._curse_env() as _:
            self._loop()

    def _loop(self):
        win = curses.newwin(20, 60, 0, 0)
        win.keypad(1)
        win.border(0)
        win.nodelay(1)

        key = curses.KEY_RIGHT
        score = 0

        # Initial snake co-ordinates
        snake = [[4, 10], [4, 9], [4, 8]]
        # First food co-ordinates
        food = [10, 20]

        # Prints the food
        win.addch(food[0], food[1], '*')
        # While Esc key is not pressed
        while key != 27:                                              
            win.border(0)
            # Printing 'Score' and
            win.addstr(0, 2, 'Score : ' + str(score) + ' ')
            # 'SNAKE' strings
            win.addstr(0, 27, ' SNAKE ')
            # Increases the speed of Snake as its length increases
            win.timeout(150 - (len(snake)/5 + len(snake)/10) % 120)

            # Previous key pressed
            prevKey = key
            event = win.getch()
            key = key if event == -1 else event

            # If SPACE BAR is pressed, wait for another
            if key == ord(' '):
                # one (Pause/Resume)
                key = -1
                while key != ord(' '):
                    key = win.getch()
                key = prevKey
                continue

            # If an invalid key is pressed
            if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, 27]:
                key = prevKey

            # Calculates the new coordinates of the head of the snake. NOTE: len(snake) increases.
            # This is taken care of later at [1].
            snake.insert(0, [snake[0][0] + (key == curses.KEY_DOWN and 1) + (key == curses.KEY_UP and -1),
                             snake[0][1] + (key == curses.KEY_LEFT and -1) + (key == curses.KEY_RIGHT and 1)])

            # If snake crosses the boundaries, make it enter from the other side
            if snake[0][0] == 0:
                snake[0][0] = 18
            if snake[0][1] == 0:
                snake[0][1] = 58
            if snake[0][0] == 19:
                snake[0][0] = 1
            if snake[0][1] == 59:
                snake[0][1] = 1

            # Exit if snake crosses the boundaries (Uncomment to enable)
            # if snake[0][0] == 0 or snake[0][0] == 19 or snake[0][1] == 0 or snake[0][1] == 59: break

            # If snake runs over itself
            if snake[0] in snake[1:]:
                break

            # When snake eats the food
            if snake[0] == food:
                food = []
                score += 1
                while food == []:
                    # Calculating next food's coordinates
                    food = [random.randint(1, 18), random.randint(1, 58)]
                    if food in snake:
                        food = []
                win.addch(food[0], food[1], '*')
            else:
                # [1] If it does not eat the food, length decreases
                last = snake.pop()
                win.addch(last[0], last[1], ' ')
            win.addch(snake[0][0], snake[0][1], '#')
        print("\nScore - " + str(score))

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
    logging.basicConfig(level=logging.INFO)
    # Snake()
    SnakeStateMachine()

if __name__ == "__main__":
    main()
