from AbstractDailyProblem import AbstractDailyProblem


opes = {
	'+': lambda u, v: u + v,
	'-': lambda u, v: u - v,
	'*': lambda u, v: u * v,
	'/': lambda u, v: u / v
}

de_opes = {
	'+': lambda u, v: u - v,
	'-': lambda u, v: u + v,
	'*': lambda u, v: u / v,
	'/': lambda u, v: u * v
}

inv_opes = {
	'+': lambda u: u,
	'-': lambda u: -u,
	'*': lambda u: u,
	'/': lambda u: 1/u
}


def shout(variables, var_name):
	if type(variables[var_name]) is int:
		return variables[var_name]
	left, ope, right = variables[var_name]
	res = opes[ope](shout(variables, left), shout(variables, right))
	variables[var_name] = res
	return int(res)


class Advent2022day21(AbstractDailyProblem):

	def parse_entry(self, entry: str):
		res, ope = entry.strip().split(': ')  # type: str, str
		if ope.isnumeric():
			return res, int(ope)
		left, ope, right = ope.split()
		return res, left, ope, right

	def parse(self, input_path: str, entry_separator='\n'):
		variables = super().parse(input_path, entry_separator)
		return {var: (ope[0] if len(ope) == 1 else ope) for var, *ope in variables}

	def question_1(self, input_path) -> int:
		variables = self.parse(input_path)
		return int(shout(variables, 'root'))

	def question_2(self, input_path) -> int:
		operations = self.parse(input_path)
		variables = operations.copy()

		def involve_human(var_name):
			if var_name == 'humn':
				return True
			if type(variables[var_name]) in [int, float]:
				return False
			else:
				left, _, right = variables[var_name]
				return involve_human(left) or involve_human(right)

		def resolve(var_name, target_value):
			if var_name == 'humn':
				return target_value
			left, op, right = variables[var_name]
			if involve_human(left):
				right_value = shout(variables, right)
				return resolve(left, de_opes[op](target_value, right_value))
			else:
				left_value = shout(variables, left)
				return resolve(right, de_opes[op](inv_opes[op](target_value), left_value))

		left_root, _, right_root = variables['root']
		if involve_human(left_root):
			return int(resolve(left_root, shout(variables, right_root)))
		return int(resolve(right_root, shout(variables, left_root)))

	def __init__(self):
		super().__init__(152, 301)


if __name__ == '__main__':
	Advent2022day21().run('../resources/2022/21/test.txt', '../resources/2022/21/input.txt')
