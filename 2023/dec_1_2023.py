import re

from AbstractDailyProblem import AbstractDailyProblem

str_digits: dict[str, int] = {
	'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9
}
str_digits.update({str(digit): digit for digit in range(1, 10)})


class Advent2023day1(AbstractDailyProblem):

	def question_1(self, input_path) -> int:
		def line_res(line: str):
			digit_chars = [_ for _ in line if _.isnumeric()]
			if len(digit_chars) == 1:
				line_res = digit_chars[0] * 2
			else:
				line_res = digit_chars[0] + digit_chars[-1]
			return int(line_res)

		lines = self.parse(input_path)
		return sum(map(line_res, lines))

	def question_2(self, input_path) -> int:
		def line_res(line: str):
			first_match = None
			last_match = None
			for start_index in range(len(line)):
				sub_line = line[start_index:]
				for str_digit, int_digit in str_digits.items():
					if sub_line.startswith(str_digit):
						if first_match is None:
							first_match = int_digit
						last_match = int_digit

			return 10 * first_match + last_match

		lines = self.parse(input_path.replace('test', 'test2'))
		return sum(map(line_res, lines))

	def __init__(self):
		super().__init__(142, 281)


if __name__ == '__main__':
	Advent2023day1().run('../resources/2023/1/test.txt', '../resources/2023/1/input.txt')
