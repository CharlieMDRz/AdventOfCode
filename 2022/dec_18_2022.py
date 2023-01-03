import itertools
from typing import Set, Tuple, List

from AbstractDailyProblem import AbstractDailyProblem


Point = Tuple[int, int, int]

sides = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def connected_components(points: Set[Point]) -> List[Set[Point]]:
	explored = set()
	components = []
	while points.difference(explored):
		to_explore = {points.pop()}
		component = set()
		while to_explore:
			comp_rep = x, y, z = to_explore.pop()
			for dx, dy, dz in sides:
				neighbour = (x + dx, y + dy, z + dz)
				if neighbour not in explored and neighbour in points:
					to_explore.add((x + dx, y + dy, z + dz))
			explored.add(comp_rep)
			component.add(comp_rep)
		components.append(component)
	return components


class Advent2022day18(AbstractDailyProblem):

	def parse_entry(self, entry: str):
		return tuple(map(int, entry.strip().split(',')))

	def question_1(self, input_path) -> int:
		cubes = set(self.parse(input_path))
		surface = 0
		for x, y, z in cubes:
			for dx, dy, dz in sides:
				if (x + dx, y + dy, z + dz) not in cubes:
					surface += 1
		return surface

	def question_2(self, input_path) -> int:
		cubes = set(self.parse(input_path))
		side_range = [-1, 0, 1]

		mesh = set()
		for x, y, z in cubes:
			for dx, dy, dz in itertools.product(side_range, side_range, side_range):
				mesh.add((x + dx, y + dy, z + dz))
		mesh.difference_update(cubes)

		components: List[Set[Point]] = connected_components(mesh)
		exterior = max(components, key=len)

		surface = 0
		for x, y, z in cubes:
			for dx, dy, dz in sides:
				if (x + dx, y + dy, z + dz) in exterior:
					surface += 1
		return surface

	def __init__(self):
		super().__init__(64, 58)


if __name__ == '__main__':
	Advent2022day18().run('../resources/2022/18/test.txt', '../resources/2022/18/input.txt')
