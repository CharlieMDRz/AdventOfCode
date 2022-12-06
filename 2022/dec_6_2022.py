from AbstractDailyProblem import AbstractDailyProblem


class Advent2022day6(AbstractDailyProblem):

	def __init__(self):
		super().__init__(10, 29)

	def parse(self, input_path, entry_separator='\n'):
		return super().parse(input_path, entry_separator)[0]

	@staticmethod
	def first_distinct_sequence(word: str, length: int) -> int:
		return next(i for i in range(length, len(word)) if len(set(word[i-length:i])) == length)

	def question_1(self, input_path) -> int:
		return self.first_distinct_sequence(self.parse(input_path), 4)

	def question_2(self, input_path) -> int:
		return self.first_distinct_sequence(self.parse(input_path), 14)


if __name__ == '__main__':
	Advent2022day6().run("../resources/2022/6/test.txt", "../resources/2022/6/input.txt")
