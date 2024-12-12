import functools

from AbstractDailyProblem import AbstractDailyProblem
from utils import Coord2D, neighbours


@functools.cache
def trailheads_from(pos: Coord2D, grid, q2: bool = False) -> set[Coord2D]:
	value_at_pos = grid[pos.i][pos.j]
	if value_at_pos == 9:
		return 1 if q2 else {pos}
	else:
		next_trail_pos = [neigh for neigh in neighbours(pos, grid) if grid[neigh.i][neigh.j] == value_at_pos + 1]
		if q2:
			return sum(trailheads_from(neigh, grid, q2) for neigh in next_trail_pos)
		else:
			return set().union(*(trailheads_from(neigh, grid, q2) for neigh in next_trail_pos))


class Advent2024day10(AbstractDailyProblem):

	def __init__(self, q1_test_answer, q2_test_answer):
		super().__init__(q1_test_answer, q2_test_answer)

	def parse_entry(self, entry: str):
		return tuple(map(int, super().parse_entry(entry)))

	def question_1(self, input_path) -> int:
		data = self.parse(input_path)
		trail_starts = [Coord2D(i, j) for i in range(len(data)) for j in range(len(data[0])) if data[i][j] == 0]
		return sum(len(trailheads_from(p, data)) for p in trail_starts)

	def question_2(self, input_path) -> int:
		data = self.parse(input_path)
		trail_starts = [Coord2D(i, j) for i in range(len(data)) for j in range(len(data[0])) if data[i][j] == 0]
		return sum(trailheads_from(p, data, True) for p in trail_starts)


if __name__ == '__main__':
	Advent2024day10(36, 81).run('../resources/2024/10/test.txt', '../resources/2024/10/input.txt')
