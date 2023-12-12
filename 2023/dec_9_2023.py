from AbstractDailyProblem import AbstractDailyProblem


def diff_signals(signal: list[int])	-> list[list[int]]:
	diff_signals = [signal]
	while not all(v == 0 for v in diff_signals[-1]):
		s = diff_signals[-1]
		diff_signals.append([s[i+1] - s[i] for i in range(len(s)-1)])
	return diff_signals


def forecast_next_value(signal: list[int]) -> int:
	res = 0
	for s in reversed(diff_signals(signal)):
		res = res + s[-1]
	return res


def forecast_prev_value(signal: list[int]) -> int:
	res = 0
	for s in reversed(diff_signals(signal)):
		res = s[0] - res
	return res


class Advent2023day9(AbstractDailyProblem):

	def __init__(self):
		super().__init__(114, 2)

	def parse_entry(self, entry: str):
		return list(map(int, entry.split(' ')))

	def question_1(self, input_path) -> int:
		signals = self.parse(input_path)
		return sum(forecast_next_value(s) for s in signals)

	def question_2(self, input_path) -> int:
		signals = self.parse(input_path)
		return sum(forecast_prev_value(s) for s in signals)


if __name__ == '__main__':
	Advent2023day9().run('../resources/2023/9/test.txt', '../resources/2023/9/input.txt')
