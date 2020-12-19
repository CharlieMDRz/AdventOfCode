def question1(dx, dy):
	forest = read_input()
	width, length = len(forest), len(forest[0])

	pos_x, pos_y = 0, 0
	encountered_trees = 0
	while pos_x < width:
		encountered_trees += forest[pos_x][pos_y] == '#'
		pos_x += dx
		pos_y = (pos_y + dy) % length

	return encountered_trees


def question2():
	result = 1
	for dx, dy in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]:
		part_result = question1(dx, dy)
		print(dx, dy, part_result)
		result *= part_result
	return result


def read_input():
	forest = [_[:-1] for _ in open("input.txt", "r").readlines()]
	return forest

if __name__ == "__main__":
	from time import time
	t0 = time()
	print("Answer #1: ", question1(1, 3))
	print("Answer #2: ", question2())
	print("Solved in {:0.3}ms".format(1000 * (time() - t0)))
