import re
from typing import Tuple, List, Union

from AbstractDailyProblem import AbstractDailyProblem


R = lambda di, dj: (dj, -di)
L = lambda di, dj: (-dj, di)


class Tiles:
	def __init__(self, pattern):
		self.pattern = pattern
		self.rows = len(pattern)
		self.cols = max(len(line) for line in pattern)
		self.row_bounds = [
			(
				next(j for j in range(len(self.pattern[i])) if pattern[i][j] != ' '),
				next(j for j in range(len(self.pattern[i])-1, -1, -1) if pattern[i][j] != ' ')
			) for i in range(self.rows)
		]
		self.col_bounds = [
			(
				next(i for i in range(self.rows) if j < len(pattern[i]) and pattern[i][j] != ' '),
				next(i for i in range(self.rows-1, -1, -1) if j < len(pattern[i]) and pattern[i][j] != ' ')
			) for j in range(self.cols)
		]

	def __getitem__(self, item):
		return self.pattern[item]


def move_to(tiles: Tiles, row, col, next_row, next_col):
	if next_row != row:
		min_row, max_row = tiles.col_bounds[col]
		if next_row > max_row:
			next_row = min_row
		if next_row < min_row:
			next_row = max_row
	if next_col != col:
		min_col, max_col = tiles.row_bounds[next_row]
		if next_col > max_col:
			next_col = min_col
		if next_col < min_col:
			next_col = max_col
	if 0 <= next_row < tiles.rows and 0 <= next_col < len(tiles[next_row]):
		if tiles[next_row][next_col] == '#':
			return row, col
		if tiles[next_row][next_col] == '.':
			return next_row, next_col
	return move_to(tiles, row, col, next_row, next_col)


class Advent2022day22(AbstractDailyProblem):

	def parse(self, input_path: str, entry_separator='\n') -> Tuple[Tiles, List[Union[int, str]]]:
		tiles, moves_str = open(input_path).read().strip('\n').split('\n\n')
		tiles = Tiles(list(map(list, tiles.split('\n'))))
		moves = re.findall('[0-9]+|[LR]', moves_str)
		moves = [int(s) if s.isnumeric() else s for s in moves]
		return tiles, moves

	def question_1(self, input_path) -> int:
		tiles, moves = self.parse(input_path)
		if 'test' in input_path:
			print(tiles.pattern, moves)
		path = [[s for s in row] for row in tiles.pattern]
		row = 0
		col = tiles[row].index('.')
		d_row, d_col = 0, 1
		for move in moves:
			if type(move) is int:
				for _ in range(move):
					path[row][col] = {(1, 0): 'v', (0, 1): '>', (-1, 0): '^', (0, -1): '<'}[d_row, d_col]
					row, col = move_to(tiles, row, col, row + d_row, col + d_col)
					path[row][col] = {(1, 0): 'v', (0, 1): '>', (-1, 0): '^', (0, -1): '<'}[d_row, d_col]
			elif move == 'R':
				d_row, d_col = R(d_row, d_col)
			elif move == 'L':
				d_row, d_col = L(d_row, d_col)

		if 'test' in input_path:
			print('\n'.join(map(''.join, path)))

		facing = {(1, 0): 1, (0, 1): 0, (-1, 0): 3, (0, -1): 2}[d_row, d_col]
		return 1000 * (row + 1) + 4 * (col + 1) + facing

	def question_2(self, input_path) -> int:
		pass

	def __init__(self):
		super().__init__(6032, 0)


if __name__ == '__main__':
	Advent2022day22().run('../resources/2022/22/test.txt', '../resources/2022/22/input.txt')
