from AbstractDailyProblem import AbstractDailyProblem


coordinate = tuple[int, int]

def find_source(network: list[str]) -> coordinate:
	for i, row in enumerate(network):
		for j, value in enumerate(row):
			if value == 'S':
				return i, j
			
			
def loop_points(network, source) -> set[coordinate]:
	seen_points = set()
	points_to_explore = [(source, 0)]

	while points_to_explore:
		point, distance = points_to_explore.pop(0)
		seen_points.add(point)
		neighbours = get_neighbours(network, point)
		if all(n in seen_points for n in neighbours):
			return seen_points
		else:
			for neigh in neighbours:
				if neigh not in seen_points:
					points_to_explore.append((neigh, distance + 1))

	return set()


def get_neighbours(network, point) -> set[coordinate]:
	x, y = point
	if not (0 <= x < len(network) and 0 <= y < len(network[0])):
		return set()
	point_char = network[x][y]
	if point_char == '|':
		return {(x-1, y), (x+1, y)}
	elif point_char == '-':
		return {(x, y-1), (x, y+1)}
	elif point_char == 'L':
		return {(x-1, y), (x, y+1)}
	elif point_char == 'J':
		return {(x-1, y), (x, y-1)}
	elif point_char == '7':
		return {(x+1, y), (x, y-1)}
	elif point_char == 'F':
		return {(x+1, y), (x, y+1)}
	elif point_char == 'S':
		return {_ for _ in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)] if point in get_neighbours(network, _)}
	else:
		return set()


class Advent2023day10(AbstractDailyProblem):

	def __init__(self):
		super().__init__(8, 1)

	def question_1(self, input_path) -> int:
		network = self.parse(input_path)
		loop = loop_points(network, find_source(network))
		return len(loop) // 2

	def question_2(self, input_path) -> int:
		network = self.parse(input_path)
		n_rows = len(network)
		n_cols = len(network[0])
		res = 0

		loop = loop_points(network, find_source(network))
		coordinates_to_explore = {(x, y) for x in range(n_rows) for y in range(n_cols)}.difference(loop)

		while coordinates_to_explore:
			connected_component = set()
			to_explore_in_component = {coordinates_to_explore.pop()}
			while to_explore_in_component:
				x, y = point = to_explore_in_component.pop()
				connected_component.add(point)
				to_explore_in_component.update(
					{(x1, y1) for x1, y1 in {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)} if 0 <= x1 < n_rows and 0 <= y1 < n_cols}
					.difference(loop)
					.difference(connected_component)
				)
			coordinates_to_explore.difference_update(connected_component)
			if all(0 < x < n_rows-1 and 0 < y < n_cols - 1 for x, y in connected_component):
				res += len(connected_component)

		return res

	def run(self, test_path="test.txt", input_path="input.txt") -> bool:
		test_folder = '../resources/2023/10'
		for test_file in ('test.txt', 'test2.txt', 'test3.txt', 'test4.txt'):
			test_path = f"{test_folder}/{test_file}"
			print(test_path)
			print(self.question_2(test_path))


if __name__ == '__main__':
	Advent2023day10().run('../resources/2023/10/test.txt', '../resources/2023/10/input.txt')
