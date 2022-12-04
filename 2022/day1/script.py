from typing import List


def parse(input_path) -> List[List[int]]:
	data = open(input_path).read().strip()
	elves_data = data.split("\n\n")
	return [list(map(int, elf_data.split("\n"))) for elf_data in elves_data]


def question1(path):
	calories_per_elf = parse(path)
	return max(map(sum, calories_per_elf))


def question2(path):
	calories_per_elf = parse(path)
	calories_per_elf.sort(key=sum, reverse=True)
	return sum(map(sum, calories_per_elf[:3]))


if __name__ == "__main__":
	assert question1("test.txt") == 24000
	print("Answer #1: ", question1("input.txt"))
	assert question2("test.txt") == 45000
	print("Answer #2: ", question2("input.txt"))
