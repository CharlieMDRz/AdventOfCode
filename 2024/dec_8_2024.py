from AbstractDailyProblem import AbstractDailyProblem
from utils import in_grid, IntCoord


def sort_antennas(data):
	antennas = {}
	for i, row in enumerate(data):
		for j, frequency in enumerate(row):
			if frequency != '.':
				antennas.setdefault(frequency, []).append(IntCoord(i, j))
	return antennas


def get_antinodes_from_group(data, antenna_group, repeat_offset=False) -> set[IntCoord]:
	antinodes = set()
	for first_antenna in antenna_group:
		for second_antenna in antenna_group:
			if first_antenna == second_antenna:
				continue
			offset = second_antenna - first_antenna
			antinode = second_antenna + offset
			if in_grid(data, antinode):
				antinodes.add(antinode)
			if repeat_offset:
				antinodes.add(second_antenna)
				while in_grid(data, antinode):
					antinodes.add(antinode)
					antinode += offset
	return antinodes


class Advent2024day8(AbstractDailyProblem):

	def __init__(self):
		super().__init__(14, 34)

	def question_1(self, input_path) -> int:
		data = self.parse(input_path)
		antennas = sort_antennas(data)
		antinodes = set()
		for group in antennas.values():
			antinodes.update(get_antinodes_from_group(data, group))
		return len(antinodes)


	def question_2(self, input_path) -> int:
		data = self.parse(input_path)
		antennas = sort_antennas(data)
		antinodes = set()
		for group in antennas.values():
			antinodes.update(get_antinodes_from_group(data, group, True))
		print(antinodes)
		return len(antinodes)


if __name__ == '__main__':
	Advent2024day8().run('../resources/2024/8/test.txt', '../resources/2024/8/input.txt')
