import collections
import functools
from typing import Iterable

from AbstractDailyProblem import AbstractDailyProblem
from dec_7_2024 import digits


def stone_transform(number: int) -> tuple[int, ...]:
	if number == 0:
		return 1,
	elif (d := digits(number)) % 2 == 0:
		split = 10 ** (d//2)
		return number // split, number % split
	else:
		return number * 2024,


def number_of_stones_after_iterations(iterations: int, initial_values: Iterable[int]) -> int:
	number_counter = collections.Counter(initial_values)
	for _ in range(iterations):
		transformed_counter = {}
		for value, occurrences in number_counter.items():
			for transformed_value in stone_transform(value):
				transformed_counter[transformed_value] = transformed_counter.get(transformed_value, 0) + occurrences
		number_counter = transformed_counter
	return sum(number_counter.values())


class Advent2024day11(AbstractDailyProblem):

	def parse_entry(self, entry: str):
		return tuple(map(int, super().parse_entry(entry).split()))

	def question_1(self, input_path) -> int:
		initial_state = self.parse(input_path)[0]
		return number_of_stones_after_iterations(25, initial_state)

	def question_2(self, input_path) -> int:
		initial_state = self.parse(input_path)[0]
		return number_of_stones_after_iterations(75, initial_state)


if __name__ == '__main__':
	Advent2024day11(55312, 65601038650482).run('../resources/2024/11/test.txt', '../resources/2024/11/input.txt')
