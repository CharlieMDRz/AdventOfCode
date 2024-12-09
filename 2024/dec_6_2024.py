import tqdm

from AbstractDailyProblem import AbstractDailyProblem
from utils import in_grid


def move(grid, row, col, d_row, d_col):
	n_row = row + d_row
	n_col = col + d_col
	if not in_grid(grid, (n_row, n_col)) or grid[n_row][n_col] != '#':
		return (n_row, n_col), (d_row, d_col)
	else:
		return (row, col), (d_col, -d_row)


def creates_loop(grid, obstacle_pos):
	grid = [list(_) for _ in grid]
	grid[obstacle_pos[0]][obstacle_pos[1]] = '#'

	guard_pos = next((i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == '^')
	guard_dir = -1, 0

	seen_pos_dir = set()
	while in_grid(grid, guard_pos) and not (guard_pos, guard_dir) in seen_pos_dir:
		seen_pos_dir.add((guard_pos, guard_dir))
		guard_pos, guard_dir = move(grid, *guard_pos, *guard_dir)

	return (guard_pos, guard_dir) in seen_pos_dir


class Advent2024day6(AbstractDailyProblem):

	def __init__(self):
		super().__init__(41, 6)

	def question_1(self, input_path) -> int:
		grid = self.parse(input_path)
		guard_pos = next((i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == '^')
		guard_dir = -1, 0
		positions = {guard_pos}
		while in_grid(grid, guard_pos):
			guard_pos, guard_dir = move(grid, *guard_pos, *guard_dir)
			positions.add(guard_pos)
		# the guard encounters #positions - 1 different positions in grid
		return len(positions) - 1


	def question_2(self, input_path) -> int:
		grid = self.parse(input_path)
		init_guard_pos = guard_pos = next((i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == '^')
		guard_dir = -1, 0
		positions = {guard_pos}
		while in_grid(grid, guard_pos):
			guard_pos, guard_dir = move(grid, *guard_pos, *guard_dir)
			positions.add(guard_pos)
		positions.remove(guard_pos)
		positions.remove(init_guard_pos)

		return len({p for p in tqdm.tqdm(positions) if creates_loop(grid, p)})


if __name__ == '__main__':
	Advent2024day6().run('../resources/2024/6/test.txt', '../resources/2024/6/input.txt')
