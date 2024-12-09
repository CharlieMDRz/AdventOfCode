from hashlib import md5

from AbstractDailyProblem import AbstractDailyProblem


class Advent2015day4(AbstractDailyProblem):

	def question_1(self, input_path) -> int:
		key, *_ = self.parse(input_path)
		i = 1
		while not md5(bytes(key + str(i), 'utf8')).hexdigest().startswith('00000'):
			i += 1
		return i

	def question_2(self, input_path) -> int:
		if 'test' in input_path:
			return 0
		key, *_ = self.parse(input_path)
		i = 1
		while not md5(bytes(key + str(i), 'utf8')).hexdigest().startswith('000000'):
			i += 1
		return i

	def __init__(self):
		super().__init__(609043, 0)


if __name__ == '__main__':
	Advent2015day4().run('../resources/2015/4/test.txt', '../resources/2015/4/input.txt')
