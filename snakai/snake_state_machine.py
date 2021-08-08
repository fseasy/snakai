# -*- coding: utf-8 -*-
"""snake game state definitions
"""
import enum
import collections
import itertools
import logging
import random


class Direction(enum.IntEnum):
    """direction"""
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    NONE = 4


Point = collections.namedtuple('Point', "x, y")


class SnakeStateMachine(object):
    """snake-state-machine
    only keep inner status, the IO logic should be impl in the other class. 
    
    the state mainly including 3 elements:
    1. environment: should be viewed as a matrix, 
        with w = width, h = height
        the matrix is consisted of points, each has position.
        the position starts with 0. 
        so all the points should bound in: x \in [0, w), y \in [0, h)
    2. snake: could be viewed as a list of continuous points and a direction.
        snake is some continuous points in the environments. it has a direction.
    3. feed: a point in the environment.

    what's more, some extra elements is used for game:
    1. score: game score, currently equals to the food eaten
    2. steps: move steps. each update on not-ended state should increase the steps.
    """
    class InnerStatus(object):
        """inner status"""
        RUNNING = 0
        FAIL = 1
        SUCCESS = 2
        UN_INIT = 3

    def __init__(self, width, height):
        """init 
        """
        # type: collections.deque
        self.snake = None
        # type: Point
        self.food = None
        self.direction = Direction.NONE
        # type: int
        self.steps = None
        # type: float
        self.score = None
        
        self._w = width
        self._h = height
        self._status = self.InnerStatus.UN_INIT
        self._rng = random.Random()

    def is_state_ok(self) -> bool:
        """query whether current state is ok
        """
        return self._status == self.InnerStatus.RUNNING

    def update_state(self, d: Direction) -> bool:
        """
        Parameters
        ------------
        d: Direction

        Returns
        ---------
        Boolean
            whether game is ok.
        """
        def _udpate_direction():
            if not DirectionUtil.is_effective(d) or DirectionUtil.is_opposite(d, self.direction):
                return
            self.direction = d

        def _add_snake_head():
            current_head_p = self.head
            d = self.direction
            new_head = gen_next_step_point(current_head_p, d)
            # no need to check collision
            self.snake.appendleft(new_head)         

        def _is_new_head_collide():
            new_head = self.head
            # case1: new-head collide on the edge
            if new_head.x in [-1, self._w] or new_head.y in [-1, self._h]:
                return True
            # case2: new-head collide on self body
            for test_point in itertools.islice(self.snake, 1, len(self.snake)):
                if new_head == test_point:
                    return True
            return False
        
        def _has_eaten_food():
            new_head = self.head
            return new_head == self.food

        def _has_succeeded():
            return len(self.snake) == self._h * self._w

        def _update_food():
            # if snake is too long and occupies almost all space, 
            # this logic may dramatically costly
            while True:
                x = self._rng.randrange(0, self._w)
                y = self._rng.randrange(0, self._h)
                new_food = Point(x, y)
                if new_food in self.snake:
                    continue
                else:
                    break
            self.food = new_food

        if not self.is_state_ok():
            return False

        self.steps += 1
        _udpate_direction()
        
        _add_snake_head()
        if _is_new_head_collide():
            self._status = self.InnerStatus.FAIL
            return False

        if _has_eaten_food():
            self.score += 1
            if _has_succeeded():
                self._status = self.InnerStatus.SUCCESS
                return False
            _update_food()
        else:
            # remove tail to make a moving illusion
            self.snake.pop()

        return True

    def new_state(self):
        
        SNAKE_LENGTH = 3
        
        def _random_snake_head():
            """init a snake.
            left space for snake body
            """
            head_x = self._rng.randrange(SNAKE_LENGTH + 1, self._w - SNAKE_LENGTH - 1)
            head_y = self._rng.randrange(SNAKE_LENGTH + 1, self._h - SNAKE_LENGTH - 1)
            return Point(head_x, head_y)
        
        def _random_food(snake_head):
            # rand a food, can't in snake
            while True:
                x = self._rng.randrange(0, self._w)
                y = self._rng.randrange(0, self._h)
                if x == snake_head.x or y == snake_head.y:
                    # food should not be in the same x and y with snake head.
                    continue
                return Point(x, y)

        def _get_direction(snake_head, food):
            # in init, we let snake only has left & right direction
            # should head for the food in the initialization.
            return Direction.RIGHT if snake_head.x <= food.x else Direction.LEFT
        
        def _init_snake(snake_head, direction):
            # in init, only left/right direction
            tail_x_offset = -1 if direction == Direction.RIGHT else 1
            snake = collections.deque([snake_head])
            for i in range(1, SNAKE_LENGTH):
                tail = Point(snake_head.x + tail_x_offset * i, snake_head.y)
                snake.append(tail)
            return snake

        snake_head = _random_snake_head()
        food = _random_food(snake_head)
        direction = _get_direction(snake_head, food)
        snake = _init_snake(snake_head, direction)

        self.snake = snake
        self.food = food
        self.direction = direction
        self.score = 0
        self.steps = 0
        self._status = self.InnerStatus.RUNNING

    def is_success(self):
        """whether SUCCESS
        """
        return self._status == self.InnerStatus.SUCCESS

    def is_fail(self):
        """whether fail
        """
        return self._status == self.InnerStatus.FAIL

    def is_outer_point_collide2snake(self, p: Point) -> bool:
        """whether collide to the snake body?
        here we don't consider the window-edge.
        """
        for test_point in self.snake:
            if test_point == p:
                return True
        return False

    @property
    def state_width(self):
        """get width"""
        return self._w
    
    @property
    def state_height(self):
        """get height"""
        return self._h

    @property
    def head(self):
        """head"""
        return self.snake[0]

    def __str__(self):
        return f"food={self.food}, snake={self.snake}, step={self.steps}, score={self.score}"


def gen_next_step_point(p: Point, direction: Direction) -> Point:
    """generate next step point according to current point and direction
    """
    if not DirectionUtil.is_effective(direction):
        raise ValueError(f"not effective direction {direction}")
    
    x = p.x
    y = p.y
    if direction == Direction.LEFT:
        return Point(x - 1, y)
    elif direction == Direction.RIGHT:
        return Point(x + 1, y)
    elif direction == Direction.UP:
        return Point(x, y - 1)
    elif direction == Direction.DOWN:
        return Point(x, y + 1)
    
    raise ValueError(f"impossible direction [{direction}], something must wrong.")


class DirectionUtil(object):
    """direction util
    """
    _OPPOSITE_DIRECTION_SET = {
        (Direction.LEFT, Direction.RIGHT), (Direction.RIGHT, Direction.LEFT), 
        (Direction.UP, Direction.DOWN), (Direction.DOWN, Direction.UP)
    }
    _OPPOSITE_DIRECTION_MAP = dict(_OPPOSITE_DIRECTION_SET)
    _EFFECTIVE_DIRECTION = {Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN}

    @classmethod
    def get_opposite(cls, d: Direction):
        """get opposite direction
        """
        opposite_direction_dict = cls._OPPOSITE_DIRECTION_MAP
        if d not in opposite_direction_dict:
            raise ValueError(f"not effective action: {d}")
        return opposite_direction_dict[d]

    @classmethod
    def is_opposite(cls, a: Direction, b: Direction) -> bool:
        """whether a and b are the opposite directions 
        """
        return (a, b) in cls._OPPOSITE_DIRECTION_SET
    
    @classmethod
    def is_valid(cls, d: Direction) -> bool:
        """whether d is a valid direction
        """
        return d in {cls.LEFT, cls.RIGHT, cls.UP, cls.DOWN, cls.NONE}
    
    @classmethod
    def get_effective(cls) -> set:
        """get effective directions
        """
        return cls._EFFECTIVE_DIRECTION

    @classmethod
    def is_effective(cls, d: Direction) -> bool:
        """whether d is a effective direction
        """
        return d in cls.get_effective()