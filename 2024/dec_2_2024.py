from AbstractDailyProblem import AbstractDailyProblem


def is_safe_report(report: list[int]) -> bool:
	sequence_sign = report[1] - report[0]
	constant_rise = all((report[i+1] - report[i]) * sequence_sign > 0 for i in range(len(report) - 1))
	moderate_rise = all(1 <= abs(report[i+1] - report[i]) <= 3 for i in range(len(report) - 1))
	return constant_rise and moderate_rise


def is_safe_report_with_removal(report: list[int]) -> bool:
	for i in range(len(report)):
		report_copy = report.copy()
		report_copy.pop(i)
		if is_safe_report(report_copy):
			return True
	return False


class Advent2024day2(AbstractDailyProblem):

	def parse_entry(self, entry: str):
		return list(map(int, super().parse_entry(entry).split()))

	def question_1(self, input_path) -> int:
		return sum(map(is_safe_report, self.parse(input_path)))

	def question_2(self, input_path) -> int:
		return sum(map(is_safe_report_with_removal, self.parse(input_path)))

	def __init__(self):
		super().__init__(2, 4)


if __name__ == '__main__':
	Advent2024day2().run('../resources/2024/2/test.txt', '../resources/2024/2/input.txt')
