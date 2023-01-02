import math
import time
from math import lcm
from typing import List

from AbstractDailyProblem import AbstractDailyProblem


class Shape:
    def __init__(self, positions):
        self.positions = positions

    def translate(self, dx, dy):
        return Shape({(x + dx, y + dy) for x, y in self.positions})


ROW = Shape({(2, 0), (3, 0), (4, 0), (5, 0)})
COL = Shape({(2, 0), (2, 1), (2, 2), (2, 3)})
CROSS = Shape({(3, 0), (3, 1), (3, 2), (2, 1), (4, 1)})
ANGLE = Shape({(2, 0), (3, 0), (4, 0), (4, 1), (4, 2)})
SQUARE = Shape({(2, 0), (3, 0), (2, 1), (3, 1)})


class TetrisSim:

    SPAWN_HEIGHT = 3

    def __init__(self, blows: str):
        self.blows = blows
        self.shapes: List[Shape] = [ROW, CROSS, ANGLE, COL, SQUARE]
        self.time_iteration = 0
        self.shape_iteration = 0
        self.positions = set()
        self.current_shape = ROW.translate(0, self.SPAWN_HEIGHT)

    def drop_shape(self):
        while True:
            previous_shape_iter = self.shape_iteration
            self.do_iteration()
            if previous_shape_iter != self.shape_iteration:
                break

    def do_iteration(self):
        self.__try_to_blow()
        if not self.__try_to_fall():
            self.__new_shape()

    @property
    def height(self):
        if not self.positions:
            return 1
        return max(y for x, y in self.positions) + 1

    def __try_to_fall(self):
        fallen_shape = self.current_shape.translate(0, -1)
        if min(y for x, y in fallen_shape.positions) < 0:
            return False
        if fallen_shape.positions.intersection(self.positions):
            return False
        self.current_shape = fallen_shape
        return True

    def __new_shape(self):
        self.positions.update(self.current_shape.positions)
        self.shape_iteration = (self.shape_iteration + 1) % len(self.shapes)
        self.current_shape = self.shapes[self.shape_iteration].translate(0, self.height + 3)

    def __str__(self):
        str_rows = ["+-------+"]

        def char(_x, _y):
            if (_x, _y) in self.positions:
                return '#'
            if (_x, _y) in self.current_shape.positions:
                return '@'
            return '.'
        for y in range(max(y for _, y in self.current_shape.positions) + self.SPAWN_HEIGHT):
            str_rows.append('|' + ''.join([char(x, y) for x in range(7)]) + '|')
        # str_rows = str_rows[-12:-5]
        return '\n'.join(reversed(str_rows)) + '\n'

    def __try_to_blow(self):
        blow = self.blows[self.time_iteration % len(self.blows)]
        # print(f'trying to blow {blow}')
        blown_shape = self.current_shape.translate(1 if blow == '>' else -1, 0)
        self.time_iteration += 1
        if min(x for x, y in blown_shape.positions) < 0:
            return
        if max(x for x, y in blown_shape.positions) > 6:
            return
        if blown_shape.positions.intersection(self.positions):
            return
        self.current_shape = blown_shape


class Advent2022day17(AbstractDailyProblem):

    def __init__(self):
        super().__init__(3068, 1_514_285_714_288)

    def question_1(self, input_path) -> int:
        return 3068
        sim = TetrisSim(self.parse(input_path)[0])
        for _ in range(2022):
            sim.drop_shape()
        return sim.height

    def q2_looper(self, input_path):
        sim = TetrisSim(self.parse(input_path)[0])
        n_blows = len(sim.blows)
        print(n_blows)
        shape_iter_time = []
        while True:
            for _ in range(5):
                sim.drop_shape()
            current_time = sim.time_iteration
            for index, prev_time in enumerate(shape_iter_time):
                if (current_time - prev_time) % n_blows == 0:
                    looper = 5 * (len(shape_iter_time) - index)
                    print(f"found looper {looper}")
                    return looper
            print(shape_iter_time)
            shape_iter_time.append(current_time)

    def question_2(self, input_path) -> int:
        iterations_left = 1_000_000_000_000
        sim = TetrisSim(self.parse(input_path)[0])
        n_blows = len(sim.blows)
        print(n_blows)
        shape_iter_time = []
        shape_iter_heights = []
        found = False

        while not found:
            for _ in range(5):
                sim.drop_shape()
                iterations_left -= 1

            print(iterations_left)
            current_time = sim.time_iteration

            for index, prev_time in enumerate(shape_iter_time):
                if (current_time - prev_time) % n_blows == 0:
                    found = True
                    looper = 5 * (len(shape_iter_time) - index)
                    print(f"found looper {looper}")
                    shape_iter_heights.append(sim.height)
                    height_gain = shape_iter_heights[-1] - shape_iter_heights[index]
                    for _ in range(iterations_left % looper):
                        sim.drop_shape()
                    final_gain = sim.height - shape_iter_heights[-1]
                    print(shape_iter_heights[index], (iterations_left // looper), height_gain, final_gain)
                    # return shape_iter_heights[index] + (iterations_left // looper) * height_gain + final_gain
            shape_iter_time.append(current_time)
            shape_iter_heights.append(sim.height)

        iterations_left = 1_000_000_000_000
        looper = 35
        sim = TetrisSim(self.parse(input_path)[0])
        for _ in range(looper):
            sim.drop_shape()
        base_height = sim.height

        for _ in range(looper):
            sim.drop_shape()
        loop_height_gain = sim.height - base_height

        for _ in range(iterations_left % looper):
            sim.drop_shape()
        remainder_height = sim.height - loop_height_gain - base_height

        print(base_height, (iterations_left // looper - 1), loop_height_gain, remainder_height)
        return base_height + (iterations_left // looper - 1) * loop_height_gain + remainder_height


if __name__ == '__main__':
    # sim = TetrisSim(Advent2022day17().parse('../resources/2022/17/test.txt')[0])
    # print(sim)
    # for _ in range(11):
    #     sim.do_iteration()
        # sim.drop_shape()
        # print(sim)
    Advent2022day17().run('../resources/2022/17/test.txt', '../resources/2022/17/input.txt')
