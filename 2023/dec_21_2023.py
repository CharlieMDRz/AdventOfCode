from AbstractDailyProblem import AbstractDailyProblem
from utils import in_grid


def positions_reachable_from(grid: list[list[str]], pos: list[tuple[int, int]]) -> list[tuple[int, int]]:
	res = set()
	width, length = len(grid), len(grid[0])
	for i, j in pos:
		for di, dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
			dpos = i+di, j+dj
			if in_grid(grid, dpos) and grid[dpos[0]][dpos[1]] in ('.', 'S'):
				res.add(dpos)
	return res


def positions_overlap_reachable_from(grid: list[list[str]], pos: dict[tuple[int, int], int]) -> dict[tuple[int, int], int]:
	res = {}
	width, length = len(grid), len(grid[0])
	for (i, j), count in pos.items():
		for di, dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
			dpos = i+di, j+dj
			try:
				if grid[dpos[0] % width][dpos[1] % length] in ('.', 'S'):
					res[dpos] = max(count, res.get(dpos, 0))
			except IndexError:
				continue

	modulo_res = {}
	for (i, j), count in res.items():
		i %= width
		j %= length
		modulo_res[(i, j)] = modulo_res.get((i, j), 0) + count
	return modulo_res


class Advent2023day21(AbstractDailyProblem):

	def question_1(self, input_path) -> int:
		grid = self.parse(input_path)
		start_pos = next((i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == 'S')
		pos = [start_pos]
		for _ in range(64):
			pos = positions_reachable_from(grid, pos)
		return len(pos)

	def question_2(self, input_path) -> int:
		grid = self.parse(input_path)
		start_pos = next((i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == 'S')
		pos = {start_pos: 1}
		for _ in range(10):
			pos = positions_overlap_reachable_from(grid, pos)
			print(pos)
			if _ in [6, 10, 50, 100, 500, 1000, 5000]:
				print(sum(pos.values()))

	def __init__(self):
		super().__init__(42, 0)


if __name__ == '__main__':
	Advent2023day21().run('../resources/2023/21/test.txt', '../resources/2023/21/input.txt')
