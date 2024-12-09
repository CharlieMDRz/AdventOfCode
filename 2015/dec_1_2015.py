from AbstractDailyProblem import AbstractDailyProblem


class Advent2015day1(AbstractDailyProblem):

	def __init__(self):
		super().__init__(0, 0)

	def question_1(self, input_path) -> int:
		characters = self.parse(input_path)[0]
		floor = 0
		for character in characters:
			if character == '(':
				floor += 1
			elif character == ')':
				floor -= 1
			else:
				raise ValueError(f'what\'s {character}')
		return floor

	def question_2(self, input_path) -> int:
		characters = self.parse(input_path)[0]
		floor = 0
		for char_index, character in enumerate(characters):
			if character == '(':
				floor += 1
			elif character == ')':
				floor -= 1
			else:
				raise ValueError(f'what\'s {character}')
			if floor == -1:
				return char_index + 1
		return 0


if __name__ == '__main__':
	Advent2015day1().run('../resources/2015/1/test.txt', '../resources/2015/1/input.txt')
