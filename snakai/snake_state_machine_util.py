# -*- coding: utf-8 -*-
"""util for ssm
"""
import itertools

from . import snake_state_machine as ssm

class DistanceCalc(object):
    """distance calculator
    """
    def __init__(self, state: ssm.SnakeStateMachine):
        self._s = state
        # used for distance calculation helper
        self._key_points = self._prepare_key_points()

    def barrier_up_dist(self):
        """get barrier up distance
        Returns:
           int (>= 0)
        """
        head = self._s.head
        x_axis_points = self._key_points["x_axis_same2head"] 
        if not x_axis_points:
            # body all not in 1 axis, should calc to edge
            return head.y - 0
        up_points = [p for p in x_axis_points if p.y <= head.y]
        if not up_points:
            return head.y - 0
        most_lower_point = max(up_points, key=lambda p: p.y)
        return head.y - most_lower_point.y

    def barrier_down_dist(self):
        """barrier down distance
        Returns:
            int (>= 0)
        """
        head = self._s.head
        x_axis_points = self._key_points["x_axis_same2head"]
        if not x_axis_points:
            return self._s.state_height - head.y
        down_points = [p for p in x_axis_points if p.y >= head.y]
        if not down_points:
            return self._s.state_height - head.y
        most_upper_point = min(down_points, key=lambda p: p.y)
        return most_upper_point.y - head.y

    def barrier_left_dist(self):
        """barrier left distance
        Returns:
            int (>= 0)
        """
        head = self._s.head
        y_axis_points = self._key_points["y_axis_same2head"]
        if not y_axis_points:
            return head.x - 0
        left_points = [p for p in y_axis_points if p.x <= head.x]
        if not left_points:
            return head.x - 0
        most_right_point = max(left_points, key=lambda p: p.x)
        return head.x - most_right_point.x

    def barrier_right_dist(self):
        """barrier right distance
        Returns:
            int (>= 0)
        """
        head = self._s.head
        y_axis_points = self._key_points["y_axis_same2head"]
        if not y_axis_points:
            return self._s.state_width - head.x
        right_points = [p for p in y_axis_points if p.x >= head.x]
        if not right_points:
            return self._s.state_width - head.x
        most_left_point = min(right_points, key=lambda p: p.x)
        return most_left_point.x - head.x
    
    def food_dist_with_sign(self):
        """head to food distance
        for distinguish 
            food <---- head
            head -----> food
        we use the `+-` sign.

        Returns:
            (x-dist-with-sign, y-dist-with-sign)
        """
        food = self._s.food
        head = self._s.head
        x_dist = head.x - food.x
        y_dist = head.y - food.y
        return (x_dist, y_dist)

    def _prepare_key_points(self):
        snake = self._s.snake
        head = snake[0]
        # you can't use islice(x, 1, stop=None) because islice is c-impl function
        # not python, so can't use keyword arguments. same as `range`
        # see https://stackoverflow.com/questions/28926633/
        #     why-i-cannot-use-keyword-argument-on-range-function
        same_x_axis_points = [p for p in itertools.islice(snake, 1, None)
            if p.x == head.x]
        same_y_axis_points = [p for p in itertools.islice(snake, 1, None)
            if p.y == head.y]

        return {
            "x_axis_same2head": same_x_axis_points,
            "y_axis_same2head": same_y_axis_points
        }
