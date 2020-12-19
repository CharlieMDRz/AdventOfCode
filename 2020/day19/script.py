def read_data(path="input.txt"):
	data = open(path).read()
	rules, words = data.split("\n\n")
	max_index = max(int(line.split(':')[0]) for line in rules.split('\n'))
	rule_set = [[] for _ in range(max_index + 1)]
	for rule in rules.split('\n'):
		index, rule = rule.split(': ')
		try:
			rule_set[int(index)] = [list(map(int, _.split())) for _ in rule.split(' | ')]
		except ValueError:
			rule_set[int(index)] = rule[1]
	words = words.split('\n')
	return rule_set, words


def fit_rules(rule_set, word: str, rule_stack: list = None) -> bool:
	if rule_stack is None:
		rule_stack = [0]  # initialize stack
	elif not rule_stack:
		return word == ""  # final check if word belongs to the grammar

	index = rule_stack.pop(0)
	if type(rule_set[index]) is str:
		return word.startswith(rule_set[index]) and fit_rules(rule_set, word[1:], rule_stack)
	else:
		return any(fit_rules(rule_set, word, _ + rule_stack) for _ in rule_set[index])


def question1(path):
	rule_set, words = read_data(path)
	return sum(fit_rules(rule_set, word) for word in words)


if __name__ == "__main__":
	print(read_data('test.txt'))
	print("Answer #1: ", question1("input.txt"))
	print("Answer #2: ", question1("input2.txt"))
