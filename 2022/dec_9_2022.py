import math
from collections import namedtuple

from AbstractDailyProblem import AbstractDailyProblem


Point = namedtuple('Point', ['x', 'y'])


def distance(p1: Point, p2: Point) -> float:
	return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


class System:
	def __init__(self, tail_count: int = 1):
		self.rope_positions = [Point(0, 0) for _ in range(tail_count + 1)]
		self.minx = self.maxx = self.miny = self.maxy = 0

	def do_iteration(self, head_movement: Point):
		head_pos = self.rope_positions[0]
		new_rope_pos = [Point(head_pos.x + head_movement.x, head_pos.y + head_movement.y)]
		for i in range(1, len(self.rope_positions)):
			new_rope_tail, prev_pos = new_rope_pos[-1], self.rope_positions[i]
			rope_dist = distance(new_rope_tail, prev_pos)
			if rope_dist < 2:
				new_rope_pos.append(prev_pos)  # no need to move
			elif rope_dist == 2:
				new_rope_pos.append(Point((new_rope_tail.x + prev_pos.x) // 2, (new_rope_tail.y + prev_pos.y) // 2))
			else:
				new_rope_tail = self.rope_positions[i]
				possible_new_p = [Point(new_rope_tail.x+1, new_rope_tail.y+1), Point(new_rope_tail.x+1, new_rope_tail.y-1), Point(new_rope_tail.x-1, new_rope_tail.y+1), Point(new_rope_tail.x-1, new_rope_tail.y-1)]
				new_rope_pos.append(min(possible_new_p, key=lambda p: distance(new_rope_pos[-1], p)))
		self.rope_positions = new_rope_pos
		self.minx = min(self.minx, min([_.x for _ in self.rope_positions]))
		self.maxx = max(self.maxx, max([_.x for _ in self.rope_positions]))
		self.miny = min(self.miny, min([_.y for _ in self.rope_positions]))
		self.maxy = max(self.maxx, max([_.y for _ in self.rope_positions]))

	def __str__(self):
		# initialize str grid as 2D char matrix
		grid = [['.' for _ in range(self.minx, self.maxx + 1)] for _ in range(self.miny, self.maxy + 1)]

		# points to mark are head of the rope + rope tail + origin
		points = self.rope_positions + [Point(0, 0)]
		labels = ['H'] + list(map(str, range(1, len(self.rope_positions)))) + ['s']
		# the `reversed` allows to overwrite further points in the list
		for point, label in zip(reversed(points), reversed(labels)):
			grid[point.y - self.miny][point.x - self.minx] = label

		return "\n".join(map("".join, grid)) + "\n\n"


class Advent2022day9(AbstractDailyProblem):

	def parse_entry(self, entry):
		direction, count = entry.split(' ')
		count = int(count)

		dir_to_vec = {
			'R': Point(1, 0),
			'L': Point(-1, 0),
			'U': Point(0, -1),
			'D': Point(0, 1)
		}
		return dir_to_vec[direction], count

	def question_1(self, input_path, tail_count=1, do_print=False) -> int:
		moves = self.parse(input_path)
		system = System(tail_count)
		tail_positions = {system.rope_positions[-1]}
		for move, count in moves:
			if do_print:
				print(move, count)
			for _ in range(count):
				system.do_iteration(move)
				tail_positions.add(system.rope_positions[-1])
			if do_print:
				print(system)
		return len(tail_positions)

	def question_2(self, input_path, do_print=False) -> int:
		return self.question_1(input_path, 9, do_print)

	def __init__(self):
		super().__init__(13, 1)


if __name__ == '__main__':
	solutions = Advent2022day9()
	solutions.run('../resources/2022/9/test.txt', '../resources/2022/9/input.txt')

	# Second test for question 2
	test_path2 = "../resources/2022/9/test2.txt"
	try:
		assert solutions.question_2(test_path2, False) == 36
	except AssertionError:
		print(f"Question 2 test #2 fails: expected 36, found {solutions.question_2(test_path2)}")
