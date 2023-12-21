from AbstractDailyProblem import AbstractDailyProblem


Intervals = dict[str, tuple[int, int]]


class Clause(object):
	def __init__(self, serial_clause):
		if ':' not in serial_clause:
			self.checked_key = ''
			self.ope = None
			self.threshold = None
			self.result = serial_clause
		else:
			check, self.result = serial_clause.split(':')
			for ope in ['>', '<']:
				if ope in check:
					self.checked_key, self.threshold = check.split(ope)
					self.threshold = int(self.threshold)
					self.ope = ope

	def test(self, **kwargs):
		if not self.ope:
			return True
		else:
			value = kwargs[self.checked_key]
			if self.ope == '>':
				return value > self.threshold
			elif self.ope == '<':
				return value < self.threshold
			else:
				raise ValueError()

	def split(self, valid_values: Intervals) -> tuple[Intervals, Intervals]:
		matching_values = {k: v for k, v in valid_values.items()}
		other_values = {k: v for k, v in valid_values.items()}
		if not self.ope:
			return valid_values, {}
		else:
			lower, upper = matching_values[self.checked_key]
			t = self.threshold
			if self.ope == '<':
				matching_values[self.checked_key] = lower, (min(t - 1, upper) if lower <= t else lower - 1)
				other_values[self.checked_key] = (max(t, lower) if t <= upper else upper + 1), upper

			elif self.ope == '>':
				matching_values[self.checked_key] = (max(t + 1, lower) if t >= lower else upper + 1), upper
				other_values[self.checked_key] = lower, (min(t, upper) if lower <= t else lower - 1)

			return matching_values, other_values


class Workflow(object):
	def __init__(self, serial_inst):
		name, clauses = serial_inst.strip()[:-1].split('{')
		self.name = name
		self.clauses = list(map(Clause, clauses.split(',')))

	def __call__(self, *args, **kwargs):
		for clause in self.clauses:
			if clause.test(**kwargs):
				return clause.result
		raise ValueError()


def compute_valid_values(
		valid_values: list[Intervals],
		workflows: dict[str, Workflow],
		workflow_id: str
):
	workflow = workflows[workflow_id]
	res = []
	for clause in workflow.clauses:
		matching_values = []
		other_values = []
		for value in valid_values:
			split = clause.split(value)
			matching_values.append(split[0])
			other_values.append(split[1])
		valid_values = other_values
		if clause.result == 'A':
			res.extend(matching_values)
		elif clause.result == 'R':
			# matching values are tossed out
			pass
		else:
			res.extend(compute_valid_values(matching_values, workflows, clause.result))

	return res


class Advent2023day19(AbstractDailyProblem):

	def __init__(self):
		super().__init__(19114, 167409079868000)

	def parse(self, input_path: str, entry_separator='\n'):
		workflows, ratings = super().parse(input_path, '\n\n')
		return (
			{w.name: w for w in map(Workflow, workflows.split('\n'))},
			[{kv[0]: int(kv[2:]) for kv in rate[1:-1].split(',')} for rate in ratings.split('\n')]
		)

	def question_1(self, input_path) -> int:
		res = 0
		workflows, ratings = self.parse(input_path)
		for r in ratings:
			cur_workflow = 'in'
			while cur_workflow not in ('A', 'R'):
				cur_workflow = workflows[cur_workflow](**r)
			if cur_workflow == 'A':
				res += sum(r.values())
		return res

	def question_2(self, input_path) -> int:
		workflows, _ = self.parse(input_path)
		valid_values = [{_: (1, 4000) for _ in 'xmas'}]
		valid_values = compute_valid_values(valid_values, workflows, 'in')
		res = 0
		for value in valid_values:
			product = 1
			for a, b in value.values():
				product *= (b - a + 1)
			res += product
		return res


if __name__ == '__main__':
	Advent2023day19().run('../resources/2023/19/test.txt', '../resources/2023/19/input.txt')
