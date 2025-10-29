from AbstractDailyProblem import AbstractDailyProblem


def sort_orderings(orderings) -> dict[int, set[int]]:
	res = {}
	for x, y in orderings:
		res.setdefault(x, set()).add(y)
	return res


def is_correctly_ordered(update, orderings) -> bool:
	for page_id, page in enumerate(update):
		next_pages = update[(page_id+1):]
		if any(next_page in orderings and page in orderings[next_page] for next_page in next_pages):
			return False
	return True


def sort_update(update):
	sorted_update =	[]
	for page in update:
		page_index = max(i for i, other in enumerate(update))


class Advent2024day5(AbstractDailyProblem):

	def __init__(self):
		super().__init__(143, 0)

	def parse(self, input_path: str, entry_separator='\n'):
		raw_orderings, raw_updates = super().parse(input_path, "\n\n")
		orderings = [list(map(int, line.strip().split('|'))) for line in raw_orderings.split('\n')]
		updates = [list(map(int, line.strip().split(','))) for line in raw_updates.split('\n')]
		return sort_orderings(orderings), updates

	def question_1(self, input_path) -> int:
		orderings, updates = self.parse(input_path)
		res = 0
		for update in updates:
			if is_correctly_ordered(update, orderings):
				res += update[len(update)//2]
		return res

	def question_2(self, input_path) -> int:
		orderings, updates = self.parse(input_path)
		res = 0
		for update in updates:
			if is_correctly_ordered(update, orderings):
				update = sort_update(update)
				res += update[len(update)//2]
		return res


if __name__ == '__main__':
	Advent2024day5().run('../resources/2024/5/test.txt', '../resources/2024/5/input.txt')
