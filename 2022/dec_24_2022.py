from AbstractDailyProblem import AbstractDailyProblem


class BlizzardSim:
	def __init__(self, initial_state):
		self.states = [initial_state]

	@property
	def width(self):
		return len(self.states[-1][0])

	@property
	def height(self):
		return len(self.states[-1])

	def __update(self):
		prev_state = self.states[-1]
		self.states.append([['#' if s == '#' else '.' for s in line] for line in prev_state])
		for i, line in enumerate(prev_state):
			for j, prev_state_element in enumerate(line):
				if type(prev_state_element) is list:
					for blizzard in prev_state_element:
						self.__propagate_blizzard(i, j, blizzard)
				elif prev_state_element in ['>', 'v', '<', '^']:
					self.__propagate_blizzard(i, j, prev_state_element)

	def __propagate_blizzard(self, i, j, blizz_symbol):
		new_i, new_j = {'>': (i, j + 1), '^': (i - 1, j), '<': (i, j - 1), 'v': (i + 1, j)}[blizz_symbol]
		if new_i == 0:
			new_i = self.height - 2  # left -> right propagation
		if new_i == self.height - 1:
			new_i = 1  # right -> left propagation
		if new_j == 0:
			new_j = self.width - 2  # top -> bottom propagation
		if new_j == self.width - 1:
			new_j = 1  # bottom -> top propagation
		self.__register_blizzard_at(new_i, new_j, blizz_symbol)

	def __register_blizzard_at(self, i, j, symbol):
		state = self.states[-1]
		blizzard_state = state[i][j]
		if type(blizzard_state) is list:
			blizzard_state.append(symbol)
		elif state[i][j] != '.':
			state[i][j] = [blizzard_state, symbol]
		else:
			state[i][j] = symbol

	def __call__(self, minute: int):
		if not isinstance(minute, int):
			raise TypeError()
		if minute >= len(self.states):
			for _ in range(len(self.states), minute + 1):
				self.__update()
		return self.states[minute]

	def __str__(self):
		state = [[str(len(s)) if type(s) is list else s for s in line] for line in self.states[-1]]
		return '\n'.join(map(''.join, state))

	def neighbours(self, i, j):
		possible_neighbours = [(i, j), (i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]

		def in_bounds(coords):
			return 0 <= coords[0] < self.height and 0 <= coords[1] < self.width

		return filter(in_bounds, possible_neighbours)


def earliest_arrival(blizzards: BlizzardSim, departure_time: int, origin, target):
	to_explore = [(*origin, departure_time)]
	explored = set()
	while to_explore:
		current_position = pos_i, pos_j, minute = to_explore.pop(0)
		if current_position in explored:
			continue

		if (pos_i, pos_j) == target:
			return minute

		for next_i, next_j in blizzards.neighbours(pos_i, pos_j):
			if blizzards(minute + 1)[next_i][next_j] == '.':
				to_explore.append((next_i, next_j, minute + 1))

		explored.add(current_position)


class Advent2022day24(AbstractDailyProblem):

	def question_1(self, input_path) -> int:
		area = self.parse(input_path)
		blizzards = BlizzardSim(area)
		orig_i = 0
		orig_j = area[0].index('.')
		targ_i = len(area) - 1
		targ_j = area[targ_i].index('.')
		return earliest_arrival(blizzards, 0, (orig_i, orig_j), (targ_i, targ_j))

	def question_2(self, input_path) -> int:
		area = self.parse(input_path)
		blizzards = BlizzardSim(area)
		origin = 0, area[0].index('.')
		target = len(area) - 1, area[len(area) - 1].index('.')
		forth = earliest_arrival(blizzards, 0, origin, target)
		back = earliest_arrival(blizzards, forth, target, origin)
		return earliest_arrival(blizzards, back, origin, target)

	def __init__(self):
		super().__init__(18, 54)


if __name__ == '__main__':
	# test
	test_area = Advent2022day24().parse('../resources/2022/24/test.txt')
	test_blizzards = BlizzardSim(test_area)
	state3 = test_blizzards(3)
	print(test_blizzards)
	Advent2022day24().run('../resources/2022/24/test.txt', '../resources/2022/24/input.txt')
