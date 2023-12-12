import math
import re

from AbstractDailyProblem import AbstractDailyProblem

pattern = "([0-9A-Z]{3}) = \(([0-9A-Z]{3}), ([0-9A-Z]{3})\)"


class Advent2023day8(AbstractDailyProblem):

	def __init__(self):
		super().__init__(2, 6)

	def parse(self, input_path: str, entry_separator='\n'):
		lines = super().parse(input_path, entry_separator)
		return lines[0], {key: {'L': left, 'R': right} for key, left, right in lines[2:]}

	def parse_entry(self, entry: str):
		match = re.search(pattern, entry.strip())
		if match is None:
			return entry
		return match.groups()

	def question_1(self, input_path) -> int:
		code, element_dict = self.parse(input_path)
		element = '11A' if 'test' in input_path else 'AAA'
		target = '11Z' if 'test' in input_path else 'ZZZ'
		code_index = 0
		steps_count = 0

		while element != target:
			element = element_dict[element][code[code_index]]
			steps_count += 1
			code_index = (code_index + 1) % len(code)

		return steps_count

	def question_2(self, input_path) -> int:
		code, element_dict = self.parse(input_path)
		cycle_lengths = []
		for symbol in [k for k in element_dict if k.endswith('A')]:
			first_occurrence = None
			code_index: int = 0
			while first_occurrence is None or symbol[-1] != 'Z':
				if symbol[-1] == 'Z':
					first_occurrence = code_index
				symbol = element_dict[symbol][code[code_index%len(code)]]
				code_index += 1

			cycle_lengths.append(code_index - first_occurrence)
		return math.lcm(*cycle_lengths)


if __name__ == '__main__':
	Advent2023day8().run('../resources/2023/8/test.txt', '../resources/2023/8/input.txt')
