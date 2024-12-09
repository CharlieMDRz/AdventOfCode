from AbstractDailyProblem import AbstractDailyProblem


class Advent2015day2(AbstractDailyProblem):

	def parse_entry(self, entry: str):
		return [int(v) for v in entry.strip().split('x')]

	def __init__(self):
		super().__init__(58, 34)

	def question_1(self, input_path) -> int:
		total_surface = 0
		for l, w, h in self.parse(input_path):
			total_surface += 2*l*w + 2*l*h + 2*w*h
			total_surface += min(l*w, l*h, w*h)
		return total_surface


	def question_2(self, input_path) -> int:
		ribbon_length = 0
		for l, w, h in self.parse(input_path):
			ribbon_length += 2 * sum(sorted((l, w, h))[:2])
			ribbon_length += l * w * h
		return ribbon_length


if __name__ == '__main__':
	Advent2015day2().run('../resources/2015/2/test.txt', '../resources/2015/2/input.txt')
