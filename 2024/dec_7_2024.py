import functools
import math
import re

from AbstractDailyProblem import AbstractDailyProblem


def digits(a: int) -> int:
	return len(str(a))
	# return int(math.log10(a)) + 1


def un_concat(a: int, b: int) -> int:
	return a // 10**digits(b)


def ends_with(a: int, b: int) -> int:
	return (a - b) % 10**digits(b) == 0


def can_get_result(test: int, numbers: list[int], include_concat: bool = False) -> bool:
	*head, tail = numbers
	if not head:
		return test == tail
	else:
		return can_get_result(test / tail, head, include_concat)\
			or can_get_result(test - tail, head, include_concat)\
			or include_concat and ends_with(test, tail) and can_get_result(un_concat(test, tail), head, include_concat)


class Advent2024day7(AbstractDailyProblem):

	def parse_entry(self, entry: str):
		test_value, *numbers = map(int, re.findall(r"\d+", entry.strip()))
		return test_value, numbers

	def question_1(self, input_path: str) -> int:
		equations = self.parse(input_path)
		return sum(test for test, numbers in equations if can_get_result(test, numbers))

	def question_2(self, input_path: str) -> int:
		equations = self.parse(input_path)
		return sum(test for test, numbers in equations if can_get_result(test, numbers, True))


if __name__ == '__main__':
	Advent2024day7(3749, 11387).run('../resources/2024/7/test.txt', '../resources/2024/7/input.txt')
