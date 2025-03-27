import re

from AbstractDailyProblem import AbstractDailyProblem


def mutate_words(words: set[str], rules) -> set[str]:
	mutated_words = set()
	for word in words:
		for pattern, mutation in rules:
			for match in re.finditer(pattern, word):
				mutated_words.add(word[:match.span()[0]] + mutation + word[match.span()[1]:])
	return mutated_words


def mutate_rec(word: str, target: str, rules: set[tuple[str, str]], d=0) -> int:
	print(len(word))
	if word == target:
		return d

	transformations = [(m, rule) for rule in rules for m in re.finditer(rule[0], word)]
	if not transformations:
		return None

	for m, r in sorted(transformations, key=lambda item: (len(item[1][1]) - len(item[1][0]), item[0].span()[0])):
		if res := mutate_rec(word[:m.span()[0]] + r[1] + word[m.span()[1]:], target, rules, d+1):
			return res


class Advent2015day19(AbstractDailyProblem):

	def __init__(self):
		super().__init__(7, 6)

	def parse(self, input_path: str, entry_separator='\n'):
		return super().parse(input_path, entry_separator)

	def parse_entry(self, entry: str):
		if ' => ' in entry:
			return entry.split(" => ")
		else:
			return super().parse_entry(entry)

	def question_1(self, input_path) -> int:
		*rules, _, start_word = self.parse(input_path)
		return len(mutate_words({start_word}, rules))

	def question_2(self, input_path) -> int:
		*rules, _, medicine = self.parse(input_path)

		rules = [(mutation, pattern) for pattern, mutation in rules]

		return mutate_rec(medicine, 'e', rules)

		# mutated_words = {medicine}
		# step = 0
		# while 'e' not in mutated_words:
		# 	mutated_words = mutate_words(mutated_words, rules)
		# 	step += 1
		# 	print((step, len(mutated_words), max(map(len, mutated_words))))
		# return step


if __name__ == '__main__':
	Advent2015day19().run('../resources/2015/19/test.txt', '../resources/2015/19/input.txt')
