import itertools
from typing import List

import tqdm

from AbstractDailyProblem import AbstractDailyProblem


class Forest:
	def __init__(self, tree_heights: List[List[int]]):
		self.trees = tree_heights
		self.width = len(tree_heights)
		self.length = len(tree_heights[0])

	def is_visible(self, i: int, j: int):
		h = self.trees[i][j]
		try:
			if h > max(self.trees[_][j] for _ in range(i+1, self.width)):
				return True
			elif h > max(self.trees[_][j] for _ in range(i)):
				return True
			elif h > max(self.trees[i][_] for _ in range(j)):
				return True
			elif h > max(self.trees[i][_] for _ in range(j+1, self.length)):
				return True
			else:
				return False
		except ValueError:
			return True  # lateral position

	def scenic_score(self, i, j) -> int:
		score = 1
		for di, dj in ((1, 0), (0, 1), (-1, 0), (0, -1)):
			score *= self.viewing_distance(i, j, di, dj)
		return score

	def viewing_distance(self, i: int, j: int, di: int, dj: int) -> int:
		distance = 0
		height = self.trees[i][j]
		while True:
			i += di
			j += dj
			if not (0 <= i < self.width and 0 <= j < self.length):
				break
			distance += 1
			if height <= self.trees[i][j]:
				break
		return distance


class Advent2022day8(AbstractDailyProblem):

	def parse_entry(self, entry):
		return list(map(int, entry.strip()))

	def parse(self, input_path, entry_separator='\n') -> Forest:
		return Forest(super().parse(input_path, entry_separator))

	def question_1(self, input_path) -> int:
		forest = self.parse(input_path)
		positions = itertools.product(range(forest.width), range(forest.length))
		return len([ij for ij in positions if forest.is_visible(*ij)])

	def question_2(self, input_path) -> int:
		forest = self.parse(input_path)
		positions = itertools.product(range(forest.width), range(forest.length))
		max_score = 0
		for i, j in tqdm.tqdm(positions):
			max_score = max(max_score, forest.scenic_score(i, j))
		return max_score

	def __init__(self):
		super().__init__(21, 8)


if __name__ == '__main__':
	Advent2022day8().run('../resources/2022/8/test.txt', '../resources/2022/8/input.txt')
