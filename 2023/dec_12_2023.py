import functools

from AbstractDailyProblem import AbstractDailyProblem


@functools.cache
def number_of_arrangements(log: str, arr: tuple[int]):
	if not arr:
		return int('#' not in log)
	elif not log:
		return 0
	else:
		rec_res = 0
		if log[0] != '#':
			rec_res += number_of_arrangements(log[1:], arr)
		# try to fit arrangement at start of log
		if len(log) >= arr[0] and '.' not in log[:arr[0]] and (len(log) == arr[0] or log[arr[0]] != '#'):
			rec_res += number_of_arrangements(log[(arr[0] + 1):], arr[1:])
		return rec_res


class Advent2023day12(AbstractDailyProblem):

	def __init__(self) -> None:
		super().__init__(21, 525152)

	def parse_entry(self, entry: str) -> tuple[str, tuple[int]]:
		log, arrangements = entry.strip().split(' ')
		return log, tuple(map(int, arrangements.split(',')))

	def question_1(self, input_path) -> int:
		records = self.parse(input_path)
		return sum(number_of_arrangements(log, arr) for log, arr in records)

	def question_2(self, input_path) -> int:
		records = self.parse(input_path)
		return sum(
			number_of_arrangements('?'.join(log for _ in range(5)), arr*5)
			for log, arr in records
		)


if __name__ == '__main__':
	Advent2023day12().run('../resources/2023/12/test.txt', '../resources/2023/12/input.txt')
