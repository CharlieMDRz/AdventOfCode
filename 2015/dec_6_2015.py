import itertools
import re

from AbstractDailyProblem import AbstractDailyProblem


def coords_iter(x1, y1, x2, y2):
	return itertools.product(range(x1, x2+1), range(y1, y2+1))


class LightsGrid:
	max_x: int
	max_y: int

	def __init__(self, max_x: int, max_y: int):
		self.max_x = max_x
		self.max_y = max_y
		self.grid = [[0 for _ in range(max_y)] for _ in range(max_x)]

	def turn_on(self, x1, y1, x2, y2, q2=False):
		for x, y in coords_iter(x1, y1, x2, y2):
			if q2:
				self.grid[x][y] += 1
			else:
				self.grid[x][y] = 1

	def turn_off(self, x1, y1, x2, y2, q2=False):
		for x, y in coords_iter(x1, y1, x2, y2):
			if q2:
				self.grid[x][y] = max(0, self.grid[x][y] - 1)
			else:
				self.grid[x][y] = 0

	def toggle(self, x1, y1, x2, y2, q2=False):
		for x, y in coords_iter(x1, y1, x2, y2):
			if q2:
				self.grid[x][y] += 2
			else:
				self.grid[x][y] = 1 - self.grid[x][y]


class Advent2015day6(AbstractDailyProblem):
	pattern = re.compile(r"([a-z ]+) (\d+),(\d+) through (\d+),(\d+)")

	def __init__(self):
		super().__init__(1_000_000, 1000000)

	def parse_entry(self, entry: str):
		command = self.pattern.match(entry.strip())
		cmd_to_fct = {
			'toggle': LightsGrid.toggle,
			'turn on': LightsGrid.turn_on,
			'turn off': LightsGrid.turn_off
		}
		raw_cmd, *raw_coords = command.groups()
		return cmd_to_fct[raw_cmd], *map(int, raw_coords)

	def question_2(self, input_path: str) -> int:
		grid = LightsGrid(1000, 1000)
		for cmd, *args in self.parse(input_path):
			cmd(grid, *args, True)
		return sum(sum(row) for row in grid.grid)

	def question_1(self, input_path: str) -> int:
		grid = LightsGrid(1000, 1000)
		for cmd, *args in self.parse(input_path):
			cmd(grid, *args)
		return sum(sum(row) for row in grid.grid)


if __name__ == '__main__':
	Advent2015day6().run('../resources/2015/6/test.txt', '../resources/2015/6/input.txt')
