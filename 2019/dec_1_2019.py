from AbstractDailyProblem import AbstractDailyProblem


def required_fuel(mass: int, recursive: bool) -> int:
	fuel_for_mass = mass // 3 - 2
	if fuel_for_mass <= 0:
		return 0
	elif recursive:
		return fuel_for_mass + required_fuel(fuel_for_mass, recursive)
	else:
		return fuel_for_mass


class Advent2019day1(AbstractDailyProblem):

	def question_1(self, input_path: str) -> int:
		return sum(required_fuel(m, False) for m in self.parse(input_path))

	def parse_entry(self, entry: str):
		return int(entry)

	def question_2(self, input_path: str) -> int:
		return sum(required_fuel(m, True) for m in self.parse(input_path))

	def __init__(self):
		super().__init__(33585, 50348)


if __name__ == '__main__':
	Advent2019day1().run('../resources/2019/1/test.txt', '../resources/2019/1/input.txt')
