from AbstractDailyProblem import AbstractDailyProblem


class Program:
	cycle: int = 0
	x: int = 1
	to_add: int = 0

	def begin_cycle(self, instruction):
		self.cycle += 1
		if type(instruction) is int:
			self.to_add = instruction
		else:
			self.to_add = 0

	def end_cycle(self):
		self.x += self.to_add

	def __repr__(self):
		return f"PROG #{self.cycle} - X == {self.x}"


class Advent2022day10(AbstractDailyProblem):

	def parse_entry(self, entry):
		args = entry.strip().split(' ')
		if len(args) > 1:
			args[1] = int(args[1])
		return args

	def parse(self, input_path, entry_separator='\n'):
		parsed_lines = super().parse(input_path, entry_separator)
		program = []
		for line in parsed_lines:
			program.extend(line)
		return program

	def question_1(self, input_path) -> int:
		instructions = self.parse(input_path)
		program = Program()
		res = 0
		for inst in instructions:
			program.begin_cycle(inst)

			if program.cycle % 40 == 20:
				value = program.cycle * program.x
				res += value

			program.end_cycle()
		return res

	def question_2(self, input_path) -> int:
		instructions = self.parse(input_path)
		program = Program()
		for inst in instructions:
			program.begin_cycle(inst)
			# render
			if abs(program.x % 40 - (program.cycle - 1) % 40) <= 1:
				print('#', end='')
			else:
				print('.', end='')
			if program.cycle % 40 == 0:
				print()  # newline
			program.end_cycle()
		return 0

	def __init__(self):
		super().__init__(13140, 0)


if __name__ == '__main__':
	Advent2022day10().run('../resources/2022/10/test.txt', '../resources/2022/10/input.txt')
