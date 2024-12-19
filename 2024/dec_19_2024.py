import functools

from AbstractDailyProblem import AbstractDailyProblem


@functools.cache
def is_possible_design(design: str, patterns: tuple[str]) -> bool:
	if design in patterns:
		return True
	for pattern in patterns:
		if design.startswith(pattern) and is_possible_design(design[len(pattern):], patterns):
			return True
	return False


@functools.cache
def number_of_arrangements_for_design(design: str, patterns: tuple[str]) -> int:
	if design == '':
		return 1
	return sum(
		number_of_arrangements_for_design(design[len(p):], patterns)
		for p in patterns if design.startswith(p)
	)


class Advent2024day19(AbstractDailyProblem):

	def __init__(self):
		super().__init__(6, 16)

	def parse(self, input_path: str, entry_separator='\n'):
		raw_towels, raw_designs = super().parse(input_path, '\n\n')
		towels = tuple(raw_towels.split(', '))
		designs = raw_designs.split('\n')
		return towels, designs

	def question_1(self, input_path: str) -> int:
		towels, designs = self.parse(input_path)
		return sum(is_possible_design(d, towels) for d in designs)

	def question_2(self, input_path: str) -> int:
		towels, designs = self.parse(input_path)
		return sum(number_of_arrangements_for_design(d, towels) for d in designs)


if __name__ == '__main__':
	Advent2024day19().run('../resources/2024/19/test.txt', '../resources/2024/19/input.txt')
