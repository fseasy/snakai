# -*- coding: utf-8 -*-
"""rule-based strategy
"""
import collections
import math

from . import base
from . import register
from .. import snake_state_machine as ssm


@register("rule_based")
class RuleBased(base.Strategy):
    """rule based strategy
    """
    def gen_next_action(self, game_state, _) -> base.Action:
        """gen next action according to current game-state
        """
        valid_dirs = self._get_valid_directions(game_state)
        
        if not valid_dirs:
            # no valid dirs, just go ahead...
            return base.Action.IDLE

        danger_space_dir2scores = self._score_based_on_danger_space(game_state, valid_dirs)
        food_dir2scores = self._score_based_on_food(game_state, valid_dirs)
        joint_dir2scores = _combine_scores(danger_space_dir2scores, food_dir2scores)
        # joint_dir2scores = _combine_scores(food_dir2scores)
        max_dir_score_pair = sorted(joint_dir2scores.items(), key=lambda p: (p[-1], p[0]), reverse=True)[0]
        max_direction = max_dir_score_pair[0]

        return base.Action.effective_direction2action(max_direction)


    def _get_valid_directions(self, game_state) -> list:
        """generating valid action
        """
        # 1. exclude reverse-direction action
        d = game_state.direction
        opposite_d = ssm.DirectionUtil.get_opposite(d)
        exclude_oppo_dirs = ssm.DirectionUtil.get_effective() - {opposite_d,}
        
        # 2. exclude immediately collision direction
        def _will_collide(point):
            # 1. window boder
            if point.x in [-1, game_state.state_width] or point.y in [-1, game_state.state_height]:
                return True
            # 2. snake body
            return game_state.is_outer_point_collide2snake(point)
        
        snake_head = game_state.snake[0]
        exclude_collide_dirs = [d for d in exclude_oppo_dirs 
            if not _will_collide(ssm.gen_next_step_point(snake_head, d))]
        return exclude_collide_dirs

    def _score_based_on_danger_space(self, game_state, valid_dirs) -> dict:
        """if a direction will lead to danger space, wo should down-vote this direction.
        what is danger-space?
        - will cause collision in future k steps following the same direction
        - collision only consider to the snake body.
        """
        def _create_snake_body_axis_index():
            x2ys = collections.defaultdict(list)
            y2xs = collections.defaultdict(list)
            for point in game_state.snake:
                x2ys[point.x].append(point.y)
                y2xs[point.y].append(point.x)
            x2ys = {x: sorted(ys) for (x, ys) in x2ys.items()}
            y2xs = {y: sorted(xs) for (y, xs) in y2xs.items()}
            return (x2ys, y2xs)

        def _score(step2collision: int) -> float:
            """score will be in range [-1, 0]. the closer to collision, the smaller score.
            """
            # because we have skiped the immediately collision direction.
            assert step2collision > 0
            if step2collision == math.inf:
                return 0
            return - 1 / step2collision

        def _score_direction(d, snake_x2ys, snake_y2xs):
            head = game_state.snake[0]
            # look-foward 1 step: first go 1 step according to the direction, then check the collision.
            # when infer score, we ignore the snake body changing after the step
            next_step_point = ssm.gen_next_step_point(head, d)
            # after move 1 step, test which direction would has collision. don't test opposite position.
            test_dirs = ssm.DirectionUtil.get_effective() - {d,}
            score = 0.
            x, y = next_step_point.x, next_step_point.y
            for direction in test_dirs:
                if direction == ssm.Direction.LEFT:
                    if y not in snake_y2xs:
                        step2collision = math.inf
                        continue
                    xs = snake_y2xs[y]
                    # TODO: can be optimized to use bisect
                    xs = [_x for _x in xs if _x < x]
                    if not xs:
                        step2collision = math.inf
                        continue
                    # we have forward 1 step in direction, so should plus 1 if test direction == direction
                    step2collision = x - max(xs) + (d == direction)
                elif direction == ssm.Direction.RIGHT:
                    if y not in snake_y2xs:
                        step2collision = math.inf
                        continue
                    xs = snake_y2xs[y]
                    xs = [_x for _x in xs if _x > x]
                    if not xs:
                        step2collision = math.inf
                        continue
                    step2collision = min(xs) - x + (d == direction)
                elif direction == ssm.Direction.UP:
                    if x not in snake_x2ys:
                        step2collision = math.inf
                        continue
                    ys = snake_x2ys[x]
                    ys = [_y for _y in ys if _y < y]
                    if not ys:
                        step2collision = math.inf
                        continue
                    step2collision = y - max(ys) + (d == direction)
                elif direction == ssm.Direction.DOWN:
                    if x not in snake_x2ys:
                        step2collision = math.inf
                        continue
                    ys = snake_x2ys[x]
                    ys = [_y for _y in ys if _y > y]
                    if not ys:
                        step2collision = math.inf
                        continue
                    step2collision = min(ys) - y + (d == direction)
                else:
                    raise ValueError(f"not effective direction: [{direction}], something error")
                score += _score(step2collision)
            return score

        (x2ys, y2xs) = _create_snake_body_axis_index()
        dir2scores = {}
        for direction in valid_dirs:
            score = _score_direction(direction, x2ys, y2xs)
            dir2scores[direction] = score

        return dir2scores

    def _score_based_on_food(self, game_state, valid_dirs) -> dict:
        """score in candidate {0, 1}
        if decrease the distance, score = 1
        else = 0 (don't pulish)
        """
        head = game_state.snake[0]
        food = game_state.food
        head_is_in_left = food.x - head.x > 0
        head_is_in_below = food.y - head.y < 0

        dir2score = {}
        for direction in valid_dirs:
            if direction == ssm.Direction.LEFT:
                if head_is_in_left:
                    score = 0.
                else:
                    score = 1.
            elif direction == ssm.Direction.RIGHT:
                if head_is_in_left:
                    score = 1.
                else:
                    score = 0.
            elif direction == ssm.Direction.UP:
                if head_is_in_below:
                    score = 1.
                else:
                    score = 0.
            elif direction == ssm.Direction.DOWN:
                if head_is_in_below:
                    score = 0.
                else:
                    score = 1.
            else:
                raise ValueError(f"not effective direction: [{direction}]")
            dir2score[direction] = score
        
        return dir2score


def _combine_scores(*args):
    result = {}
    for d in args:
        for k in d:
            result[k] = result.get(k, 0.) + d[k]
    return result
