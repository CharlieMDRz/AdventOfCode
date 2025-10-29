import re
from collections.abc import Callable
from typing import Optional

import attrs

from AbstractDailyProblem import AbstractDailyProblem


@attrs.define()
class TodaysComputer:
	registers: dict[str, int]

	def read_combo(self, operand: int) -> int:
		assert 0 <= operand < 7
		if operand <= 3:
			return operand
		elif operand == 4:
			return self.registers['A']
		elif operand == 5:
			return self.registers['B']
		elif operand == 6:
			return self.registers['C']

	def run(self, opcode, combo):
		return self.instructions[opcode](combo)

	def adv(self, operand):
		res = self.registers['A'] // (2 ** self.read_combo(operand))
		self.registers['A'] = res

	def bxl(self, operand):
		res = self.registers['B'] ^ operand
		self.registers['B'] = res

	def bst(self, operand):
		res = self.read_combo(operand) % 8
		self.registers['B'] = res

	def jnz(self, operand):
		if self.registers['A']:
			return operand

	def bxc(self, operand):
		self.registers['B'] = self.registers['B'] ^ self.registers['C']

	def out(self, operand):
		return self.read_combo(operand) % 8

	def bdv(self, operand):
		res = self.registers['A'] // (2 ** self.read_combo(operand))
		self.registers['B'] = res

	def cdv(self, operand):
		res = self.registers['A'] // (2 ** self.read_combo(operand))
		self.registers['C'] = res

	@property
	def instructions(self) -> list[Callable[[int], Optional[int]]]:
		return [self.adv, self.bxl, self.bst, self.jnz, self.bxc, self.out, self.bdv, self.cdv]


def custom_test():
	cmp = TodaysComputer({'C': 9})
	cmp.run(2, 6)
	assert cmp.registers['B'] == 1
	cmp = TodaysComputer({'A': 10})
	assert cmp.run(5, 0) == 0
	assert cmp.run(5, 1) == 1
	assert cmp.run(5, 4) == 2
	cmp = TodaysComputer({'B': 2024, 'C': 43690})
	cmp.run(4, 0)
	assert cmp.registers['B'] == 44354


class Advent2024day17(AbstractDailyProblem):

	def __init__(self):
		super().__init__("4,6,3,5,6,3,5,2,1,0", 117440)

	def parse(self, input_path: str, entry_separator='\n'):
		registers, program = super().parse(input_path, '\n\n')
		register_re = re.compile(r"Register (\w+): (\d+)")
		memory = {
			match.group(1): int(match.group(2)) for match in map(register_re.match, registers.split('\n'))
		}
		instructions = list(map(int, program.split()[1].split(',')))
		return memory, instructions

	def question_1(self, input_path) -> int:
		custom_test()
		memory, instructions = self.parse(input_path, '\n\n')
		output = []

		cmp = TodaysComputer(memory)

		ptr = 0
		while True:
			try:
				opcode = instructions[ptr]
				combo = instructions[ptr+1]
				res = cmp.run(opcode, combo)
				if 'test' not in input_path:
					print(f"exec instruction {opcode} w operand {combo}, got {res} - mem {cmp.registers}")
				if res is not None:
					if opcode == 3:
						ptr = res
					else:
						ptr += 2
						output.append(res)
				else:
					ptr += 2
			except IndexError:
				return ','.join(map(str, output))

	def question_2(self, input_path) -> int:
		memory, instructions = self.parse(input_path.replace('test', 'test2'), '\n\n')
		output = instructions.copy()

		cmp = TodaysComputer({'A': 0, 'B': 0, 'C': 0})

		ptr = len(instructions) - 4
		while ptr >= 0 or output:
			if ptr < 0:
				ptr = len(instructions) - 4
			opcode = instructions[ptr]
			literal = instructions[ptr+1]
			match opcode:
				case 0:
					cmp.registers['A'] *= 2 ** literal  # right ?
				case 1 | 2 | 4:
					cmp.run(opcode, literal)
				# case 2:
				# 	cmp.run(opcode, literal)
				# 	break
				# case 4:
				# 	cmp.run(opcode, literal)
				# 	break
				case 5:
					cmp.registers[{4: 'A', 5: 'B', 6: 'C'}[instructions[ptr+1]]] += output.pop(-1)
				case 6:
					cmp.registers['A'] = cmp.registers['B'] * 2 ** literal
				case 7:
					cmp.registers['A'] = cmp.registers['C'] * 2 ** literal
				case _:
					raise ValueError
			ptr -= 2
		return cmp.registers['A']


if __name__ == '__main__':
	Advent2024day17().run('../resources/2024/17/test.txt', '../resources/2024/17/input.txt')
