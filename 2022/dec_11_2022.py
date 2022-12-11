import re
from typing import List, Callable, Dict

import attr
import tqdm

from AbstractDailyProblem import AbstractDailyProblem


@attr.s(auto_attribs=True)
class Monkey:
	name: int
	items: List[int]
	operation: Callable[[int], int]
	test: Callable[[int], int]
	divisive: int


class Advent2022day11(AbstractDailyProblem):

	def parse(self, input_path, entry_separator='\n'):
		return {monkey.name: monkey for monkey in super().parse(input_path, '\n\n')}  # split around monkeys

	def parse_operation(self, operation: str) -> Callable[[int], int]:
		obj1, ope, obj2 = operation.split(' ')
		assert obj1 == 'old'
		if ope == '+':
			if obj2 == 'old':
				return lambda old: old + old
			else:
				return lambda old: old + int(obj2)
		elif ope == '*':
			if obj2 == 'old':
				return lambda old: old * old
			else:
				return lambda old: old * int(obj2)

	@staticmethod
	def do_rounds(monkeys: Dict[int, Monkey], n_rounds: int, worry_factor: int):
		base = 1
		for monkey in monkeys.values():
			base *= monkey.divisive

		inspections_per_monkey = [0 for _ in range(len(monkeys))]
		for _ in range(n_rounds):
			for n_monkey in range(len(monkeys)):
				monkey = monkeys[n_monkey]
				while monkey.items:
					inspections_per_monkey[n_monkey] += 1
					item = monkey.items.pop(0)
					item = monkey.operation(item) // worry_factor % base
					monkeys[monkey.test(item)].items.append(item)

		return inspections_per_monkey

	def parse_entry(self, entry) -> Monkey:
		monkey_lines = list(map(str.strip, entry.split('\n')))
		name = int(re.match("Monkey (\\d+):", monkey_lines[0]).group(1))
		items = list(map(int, monkey_lines[1].split(': ')[-1].split(', ')))
		operation = self.parse_operation(monkey_lines[2].split('= ')[-1])

		test_div = int(monkey_lines[3].split(' ')[-1])
		true_monkey = int(monkey_lines[4].split(' ')[-1])
		false_monkey = int(monkey_lines[5].split(' ')[-1])
		test_ope = lambda worry: true_monkey if (worry % test_div == 0) else false_monkey

		return Monkey(name, items, operation, test_ope, test_div)

	def question_1(self, input_path) -> int:
		monkeys = self.parse(input_path)
		inspections_per_monkey = self.do_rounds(monkeys, 20, 3)
		top_inspections = sorted(inspections_per_monkey, reverse=True)
		return top_inspections[0] * top_inspections[1]

	def question_2(self, input_path) -> int:
		monkeys = self.parse(input_path)
		inspections_per_monkey = self.do_rounds(monkeys, 10000, 1)
		top_inspections = sorted(inspections_per_monkey, reverse=True)
		return top_inspections[0] * top_inspections[1]

	def __init__(self):
		super().__init__(10605, 2713310158)


if __name__ == '__main__':
	Advent2022day11().run('../resources/2022/11/test.txt', '../resources/2022/11/input.txt')
