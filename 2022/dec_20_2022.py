from typing import List

from AbstractDailyProblem import AbstractDailyProblem


def mix(elements: List[int], number: int):
	index = elements.index(number)
	elements.pop(index)
	new_index = (index + number) % len(elements)
	elements.insert(new_index, number)


def get(elements: List[int], index: int):
	return elements[index % len(elements)]


class Advent2022day20(AbstractDailyProblem):

	def __init__(self):
		super().__init__(3, 1623178306)

	def parse_entry(self, entry: str):
		return int(entry.strip())

	def question_1(self, input_path) -> int:
		numbers = self.parse(input_path)
		indices = list(range(len(numbers)))
		for index in indices.copy():
			indices.pop(j := indices.index(index))
			indices.insert((j+numbers[index]) % len(indices), index)
		zero_index = indices.index(numbers.index(0))
		return sum(numbers[indices[(zero_index+p)%len(numbers)]] for p in [1000, 2000, 3000])

	def question_2(self, input_path) -> int:
		numbers = [_*811589153 for _ in self.parse(input_path)]
		indices = list(range(len(numbers)))
		for index in indices * 10:
			indices.pop(j := indices.index(index))
			indices.insert((j+numbers[index]) % len(indices), index)
		zero_index = indices.index(numbers.index(0))
		return sum(numbers[indices[(zero_index+p)%len(numbers)]] for p in [1000, 2000, 3000])



if __name__ == '__main__':
	test_list = [4, 1, 5, -1, -5, 10]
	print(test_list)
	for n in test_list.copy():
		mix(test_list, n)
		print(n, test_list)
	Advent2022day20().run('../resources/2022/20/test.txt', '../resources/2022/20/input.txt')
