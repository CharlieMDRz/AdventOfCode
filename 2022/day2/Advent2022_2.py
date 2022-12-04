from AbstractDailyProblem import AbstractDailyProblem


class Advent2022_2(AbstractDailyProblem):

	def parse(self, input_path):
		lines = open(input_path).read().strip().split("\n")
		opponent_encoder = {'A': 1, 'B': 2, 'C': 0}
		my_encoder = {'X': 1, 'Y': 2, 'Z': 0}
		return [(opponent_encoder[line[0]], my_encoder[line[2]]) for line in lines]

	@staticmethod
	def shape_score(shape):
		return [3, 1, 2][shape % 3]

	@staticmethod
	def round_score(opponent_shape, my_shape):
		return [3, 6, 0][(my_shape - opponent_shape) % 3]

	def question_1(self, input_path) -> int:
		rounds = self.parse(input_path)
		return sum(self.shape_score(x) + self.round_score(x, a) for a, x in rounds)

	def question_2(self, input_path) -> int:
		rounds = self.parse(input_path)
		score = 0
		for a, instruction in rounds:
			x = [a + 1, a - 1, a][instruction]
			score += self.shape_score(x) + self.round_score(a, x)
		return score

	def __init__(self):
		super().__init__(15, 12)


if __name__ == '__main__':
	Advent2022_2().run()
