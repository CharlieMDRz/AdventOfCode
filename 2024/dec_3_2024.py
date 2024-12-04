import re

from AbstractDailyProblem import AbstractDailyProblem


class Advent2024day3(AbstractDailyProblem):

	def __init__(self):
		super().__init__(161, 48)

	def question_1(self, input_path) -> int:
		data = self.parse(input_path)
		expressions = re.findall(r"mul\((\d+),(\d+)\)", ''.join(data))
		return sum(int(expr[0]) * int(expr[1]) for expr in expressions)

	def question_2(self, input_path) -> int:
		if 'test' in input_path:
			input_path = input_path.replace('test', 'test2')
		data = self.parse(input_path)
		mul_pattern = r"(mul)\((\d+),(\d+)\)"
		do_pattern = r"(do)\(\)"
		dont_pattern = r"(don't)\(\)"
		full_pattern = f"(?:{mul_pattern})|(?:{do_pattern})|(?:{dont_pattern})"

		expressions = re.findall(full_pattern, ''.join(data))
		mul_activated = True
		result = 0
		for expr in expressions:
			if "do" in expr:
				mul_activated = True
			elif "don't" in expr:
				mul_activated = False
			elif "mul" in expr:
				if mul_activated:
					result += int(expr[1]) * int(expr[2])
			else:
				raise NotImplementedError(str(expr))

		return result


if __name__ == '__main__':
	Advent2024day3().run('../resources/2024/3/test.txt', '../resources/2024/3/input.txt')
