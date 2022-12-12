import itertools
from collections import namedtuple, deque
from typing import List, Set, Dict, Deque

import attr

from AbstractDailyProblem import AbstractDailyProblem

Point = namedtuple('Point', ['x', 'y'])


@attr.s(auto_attribs=True)
class PathFind:
	start: Point
	end: Point
	hill: List[List[int]]

	def neighbours(self, point: Point):
		adjacent_points = [
			Point(point.x + 1, point.y), Point(point.x - 1, point.y),
			Point(point.x, point.y + 1), Point(point.x, point.y - 1)
		]

		def valid(p):
			try:
				return self.hill[p.x][p.y] <= self.hill[point.x][point.y] + 1
			except IndexError:
				return False

		return set(filter(valid, adjacent_points))

	def find_path(self, starting_points: List[Point]) -> List[Point]:
		if starting_points is None:
			starting_points = {self.start}
		to_explore: Deque[Point] = deque(starting_points)
		parent: Dict[Point, Point] = dict()
		explored: Set[Point] = set()
		current = self.start

		while current != self.end:
			current = to_explore.popleft()
			if current in explored:
				continue
			for neighbour in self.neighbours(current).difference(explored):
				to_explore.append(neighbour)
				parent.setdefault(neighbour, current)  # only the first parent is registered
			explored.add(current)

		path_to_end = []
		while current not in starting_points:
			path_to_end.append(current)
			current = parent[current]

		return path_to_end


class Advent2022day12(AbstractDailyProblem):

	def parse(self, input_path, entry_separator='\n') -> PathFind:
		raw_hill = super().parse(input_path, entry_separator)
		start = None
		end = None
		for x, hill_side in enumerate(raw_hill):  # type: int, List[str]
			if 'S' in hill_side:
				y = hill_side.index('S')
				start = Point(x, y)
				hill_side[y] = 'a'

			if 'E' in hill_side:
				y = hill_side.index('E')
				end = Point(x, y)
				hill_side[y] = 'z'

		hill = [[ord(hill_point) - ord('a') for hill_point in hill_side] for hill_side in raw_hill]
		return PathFind(start, end, hill)

	def parse_entry(self, entry):
		return list(entry)

	def question_1(self, input_path) -> int:
		hill_climb = self.parse(input_path)
		path = hill_climb.find_path([hill_climb.start])
		return len(path)

	def question_2(self, input_path) -> int:
		hill_climb = self.parse(input_path)
		height, width = len(hill_climb.hill), len(hill_climb.hill[0])
		starting_points = [Point(x, y) for x, y in itertools.product(range(height), range(width)) if hill_climb.hill[x][y] == 0]
		path = hill_climb.find_path(starting_points)
		return len(path)

	def __init__(self):
		super().__init__(31, 29)


if __name__ == '__main__':
	Advent2022day12().run('../resources/2022/12/test.txt', '../resources/2022/12/input.txt')
