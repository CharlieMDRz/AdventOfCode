import itertools
import math
from typing import Iterator

from AbstractDailyProblem import AbstractDailyProblem


class LocatedNumber(object):
	def __init__(self, x, y, value: int):
		self.value = value
		self.positions = set(neighbours(x, y, value))

def get_numbers(data: list[list[str]]) -> list[LocatedNumber]:
	for line_index, line in enumerate(data):
		in_number = False
		start_index = 0
		for char_index, char in enumerate(f'{line}.'):
			if char.isnumeric():
				if not in_number:
					# start number
					start_index = char_index
				in_number = True
			elif in_number:
				# end number
				yield LocatedNumber(line_index, start_index, int(line[start_index: char_index]))
				in_number = False


def neighbours(row: int, col: int, number: int) -> Iterator[tuple[int, int]]:
	number_length = int(math.ceil(math.log10(number)))
	return itertools.product(range(row - 1, row + 2), range(col - 1, col + number_length + 1))


def is_special_char(data, x1, y1):
	try:
		char = data[x1][y1]
		return not char.isnumeric() and char != '.'
	except IndexError:
		return False


def gear_ratio(data, numbers, x, y):
	if data[x][y] != '*':
		return 0
	else:
		neighbour_nums: list[LocatedNumber] = [n for n in numbers if (x, y) in n.positions]
		if len(neighbour_nums) == 2:
			return neighbour_nums[0].value * neighbour_nums[1].value
		else:
			return


class Advent2023day3(AbstractDailyProblem):

	def __init__(self) -> None:
		super().__init__(4361, 467835)

	def parse_entry(self, entry: str):
		return super().parse_entry(entry)

	def question_1(self, input_path) -> int:
		data = self.parse(input_path)
		return sum(n.value for n in get_numbers(data) if any(is_special_char(data, x1, y1) for x1, y1 in n.positions))

	def question_2(self, input_path) -> int:
		data = self.parse(input_path)
		numbers = list(get_numbers(data))
		return sum(gear_ratio(data, numbers, x, y) for x, y in itertools.product(range(len(data)), range(len(data[0]))))

	def run(self, test_path="test.txt", input_path="input.txt") -> bool:
		return super().run(test_path, input_path)


if __name__ == '__main__':
	Advent2023day3().run('../resources/2023/3/test.txt', '../resources/2023/3/input.txt')
