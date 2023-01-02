from collections import deque
from collections import deque
from typing import Tuple, Set, Deque

from AbstractDailyProblem import AbstractDailyProblem


def drop_sand(rocks, fall_path, depth) -> None:
	x, y = fall_path[-1]
	while y <= depth and any((x1, y+1) not in rocks for x1 in range(x-1, x+2)):
		for fall_pos in [(x, y+1), (x-1, y+1), (x+1, y+1)]:
			if fall_pos not in rocks:
				x, y = fall_pos
				fall_path.append(fall_pos)
				break


class Advent2022day14(AbstractDailyProblem):

	def parse_entry(self, entry):
		xy_list = entry.strip().split(' -> ')
		return [(int(xy[0]), int(xy[1])) for xy in map(lambda _: _.split(','), xy_list)]

	def parse(self, input_path, entry_separator='\n'):
		rock_formations = super().parse(input_path, entry_separator)
		rocks = set()
		for rock_formation in rock_formations:
			for (x1, y1), (x2, y2) in zip(rock_formation[:-1], rock_formation[1:]):
				if x1 == x2:
					rocks.update({(x1, y) for y in range(min(y1, y2), max(y1, y2) + 1)})
				else:
					rocks.update({(x, y1) for x in range(min(x1, x2), max(x1, x2) + 1)})
		return rocks

	def question_1(self, input_path) -> int:
		rocks: Set[Tuple[int, int]] = self.parse(input_path)
		counter = 0
		depth = max(rock[1] for rock in rocks)
		fall_path: Deque[Tuple[int, int]] = deque([(500, 0)])
		drop_sand(rocks, fall_path, depth)
		while fall_path[-1][1] <= depth:
			counter += 1
			rocks.add(fall_path.pop())
			drop_sand(rocks, fall_path, depth)
		return counter

	def question_2(self, input_path) -> int:
		rocks = self.parse(input_path)
		depth = max(y for _, y in rocks)
		min_x = min(x for x, _ in rocks)
		max_x = max(x for x, _ in rocks)
		rocks.update({(x, depth + 2) for x in range(min_x - depth, max_x + depth)})

		fall_path: Deque[Tuple[int, int]] = deque([(500, 0)])
		counter = 0
		while fall_path:
			drop_sand(rocks, fall_path, depth + 2)
			counter += 1
			rocks.add(fall_path.pop())
		return counter

	def __init__(self):
		super().__init__(24, 93)


if __name__ == '__main__':
	Advent2022day14().run('../resources/2022/14/test.txt', '../resources/2022/14/input.txt')
