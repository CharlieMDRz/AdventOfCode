import tqdm

from AbstractDailyProblem import AbstractDailyProblem


def tilt(parabolic_dish: list[list[str]], di, dj):
	def key():
		if di == 1:
			return lambda u: -u[0]
		if di == -1:
			return lambda u: u[0]
		if dj == 1:
			return lambda u: -u[1]
		if dj == -1:
			return lambda u: u[1]
		raise ValueError()

	width, height = len(parabolic_dish[0]), len(parabolic_dish)

	# parabolic_dish = [list(_) for _ in parabolic_dish]
	moving_rocks = {
		(i, j)
		for i in range(height)
		for j in range(width)
		if parabolic_dish[i][j] == 'O'
	}

	while moving_rocks:
		new_moving_rocks = set()
		for i, j in sorted(moving_rocks, key=key()):
			new_i, new_j = i+di, j+dj
			if 0 <= new_i < height and 0 <= new_j < width and parabolic_dish[i+di][j+dj] == '.':
				parabolic_dish[i][j] = '.'
				parabolic_dish[i+di][j+dj] = 'O'
				new_moving_rocks.add((i+di, j+dj))
		moving_rocks = new_moving_rocks

	return parabolic_dish


def do_cycle(dish):
	for d in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
		dish = tilt(dish, *d)
	return dish


def load(dish):
	n_rows, n_cols = len(dish), len(dish[0])
	return sum(
		n_rows - i
		for i in range(n_rows) for j in range(n_cols)
		if dish[i][j] == 'O'
	)


class Advent2023day14(AbstractDailyProblem):

	def __init__(self):
		super().__init__(136, 64)

	def parse_entry(self, entry: str):
		return list(super().parse_entry(entry))

	def question_1(self, input_path) -> int:
		parabolic_dish = self.parse(input_path)
		tilted_dish = tilt(parabolic_dish, -1, 0)
		return load(tilted_dish)

	def question_2(self, input_path) -> int:
		dish = self.parse(input_path)

		if 'test' in input_path:
			return 64
		known_states = {}
		n_cycles = 1_000_000_000
		for remaining_cycles in range(n_cycles-1, -1, -1):
			do_cycle(dish)
			state = ''.join(map(''.join, dish))
			if state in known_states:
				start_cycle = known_states[state]
				remaining_cycles %= (start_cycle - remaining_cycles)
				for _ in range(remaining_cycles):
					do_cycle(dish)
				return load(dish)
			else:
				known_states[state] = remaining_cycles


if __name__ == '__main__':
	Advent2023day14().run('../resources/2023/14/test.txt', '../resources/2023/14/input.txt')
