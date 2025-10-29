import numpy as np

from AbstractDailyProblem import AbstractDailyProblem


def intersect_in_bounds(first_hail, second_hail, area_min, area_max) -> bool:
	first_pos, first_vel = first_hail
	second_pos, second_vel = second_hail
	p1x, p1y, _ = first_pos
	p2x, p2y, _ = second_pos
	v1x, v1y, _ = first_vel
	v2x, v2y, _ = second_vel

	P = np.array([[p2x - p1x], [p2y - p1y]])
	V = np.array([
		[v1x, -v2x],
		[v1y, -v2y]
	])

	try:
		T = np.matmul(np.linalg.inv(V), P)
		x = p1x + T[0] * v1x
		y = p1y + T[0] * v1y
		return np.all(T >= 0) and area_min <= x <= area_max and area_min <= y <= area_max
	except np.linalg.LinAlgError:
		return False


class Advent2023day24(AbstractDailyProblem):

	def __init__(self):
		super().__init__(2, 0)

	def parse_entry(self, entry: str):
		return [[int(coord) for coord in vector.split(', ')] for vector in entry.strip().split(' @ ')]

	def question_1(self, input_path) -> int:
		hailstones = self.parse(input_path)
		area_min, area_max = (7, 27) if 'test' in input_path else (200000000000000, 400000000000000)

		intersections = 0

		for index, first_hail in enumerate(hailstones):
			for second_hail in hailstones[index+1:]:
				intersections += intersect_in_bounds(first_hail, second_hail, area_min, area_max)

		return intersections

	def question_2(self, input_path) -> int:
		pass


if __name__ == '__main__':
	Advent2023day24().run('../resources/2023/24/test.txt', '../resources/2023/24/input.txt')
