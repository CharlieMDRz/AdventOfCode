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
        return '\n'.join(reversed(str_rows)) + '\n'

    def __try_to_blow(self):
        blow = self.blows[self.time_iteration % len(self.blows)]
        blown_shape = self.current_shape.translate(1 if blow == '>' else -1, 0)
        self.time_iteration += 1
        if min(x for x, y in blown_shape.positions) < 0:
            return
        if max(x for x, y in blown_shape.positions) > 6:
            return
        if blown_shape.positions.intersection(self.positions):
            return
        self.current_shape = blown_shape

    @property
    def state(self):
        view_from_top = [max(y for x, y in self.positions if x == index) if any(x == index for x, _ in self.positions) else 0 for index in range(7)]
        offset_view_from_top = [_ - min(view_from_top) for _ in view_from_top]
        return *offset_view_from_top, self.time_iteration % len(self.blows)


class Advent2022day17(AbstractDailyProblem):

    def __init__(self):
        super().__init__(3068, 1_514_285_714_288)

    def question_1(self, input_path) -> int:
        sim = TetrisSim(self.parse(input_path)[0])
        for _ in range(2022):
            sim.drop_shape()
        return sim.height

    def question_2(self, input_path) -> int:
        iterations_left = total_iterations = 1_000_000_000_000
        sim = TetrisSim(self.parse(input_path)[0])
        seen_states = {}

        while (state := sim.state) not in seen_states:
            seen_states[state] = (sim.height, iterations_left)

            for _ in range(5):
                sim.drop_shape()
            iterations_left -= 5

        print(f"Found known state after {total_iterations - iterations_left} iterations !")
        height_at_prev_loop, iterations_left_at_prev_loop = seen_states[state]
        loop_height_gain = sim.height - height_at_prev_loop
        loop_duration = iterations_left_at_prev_loop - iterations_left
        loops_left = iterations_left // loop_duration
        print(f"It takes {loop_duration} iterations to get back to it")

        iterations_left %= loops_left
        for _ in range(iterations_left):
            sim.drop_shape()

        return sim.height + loops_left * loop_height_gain


if __name__ == '__main__':
    Advent2022day17().run('../resources/2022/17/test.txt', '../resources/2022/17/input.txt')
