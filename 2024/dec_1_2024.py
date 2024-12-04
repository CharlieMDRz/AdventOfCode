import collections

from AbstractDailyProblem import AbstractDailyProblem


class Advent2024day1(AbstractDailyProblem):

	def __init__(self):
		super().__init__(11, 31)

	def parse_entry(self, entry: str):
		return tuple(map(int, super().parse_entry(entry).split()))

	def parse(self, input_path: str, entry_separator='\n'):
		raw_data = super().parse(input_path)
		left_list = [line[0] for line in raw_data]
		right_list = [line[1] for line in raw_data]
		return left_list, right_list

	def question_1(self, input_path) -> int:
		left, right = self.parse(input_path)
		return sum(abs(a - b) for a, b in zip(sorted(left), sorted(right)))

	def question_2(self, input_path) -> int:
		left, right = self.parse(input_path)
		right_counter = collections.Counter(right)
		return sum(left_item * right_counter.get(left_item, 0) for left_item in left)


if __name__ == '__main__':
	Advent2024day1().run('../resources/2024/1/test.txt', '../resources/2024/1/input.txt')
