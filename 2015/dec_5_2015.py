from AbstractDailyProblem import AbstractDailyProblem


def is_nice(line: str):
	cond_1 = sum(_ in 'aeiou' for _ in line) >= 3
	cond_2 = any(line[i] == line[i+1] for i in range(len(line)-1))
	forbidden_sequences = ['ab', 'cd', 'pq', 'xy']
	cond_3 = all(line[i:(i+2)] not in forbidden_sequences for i in range(len(line)-1))
	return cond_1 and cond_2 and cond_3


def is_nicer(line: str):
	has_double_pair = any(line[i:(i+2)] in line[(i+2):] for i in range(len(line)-3)) if len(line)>=4 else False
	has_sandwich = any(line[i] == line[i+2] for i in range(len(line)-2))
	return has_double_pair and has_sandwich


class Advent2015day5(AbstractDailyProblem):

	def __init__(self):
		super().__init__(0, 0)

	def question_1(self, input_path: str) -> int:
		return sum(is_nice(line) for line in self.parse(input_path))

	def question_2(self, input_path: str) -> int:
		return sum(is_nicer(line) for line in self.parse(input_path))


if __name__ == '__main__':
	Advent2015day5().run('../resources/2015/5/test.txt', '../resources/2015/5/input.txt')
