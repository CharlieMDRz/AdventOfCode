def question1():
	result = 0
	group = set()
	for line in open('input.txt').readlines() + ['']:
		if len(line.strip()) == 0:
			result += len(group)
			group = set()
		else:
			group = group.union(set(c for c in line.strip()))
	return result


def question2():
	result = 0
	group = None
	for line in open('input.txt').readlines() + ['']:
		if len(line.strip()) == 0:
			result += len(group)
			group = None
		else:
			line_group = set(c for c in line.strip())
			if group is None:
				group = line_group
			group = group.intersection(line_group)
	return result


if __name__ == "__main__":
	print("Answer #1: ", question1())
	print("Answer #2: ", question2())
