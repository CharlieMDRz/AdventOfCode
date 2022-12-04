from typing import List

from AbstractDailyProblem import AbstractDailyProblem


class Advent2022day3(AbstractDailyProblem):

	def __init__(self):
		super().__init__(157, 70)

	def parse(self, input_path) -> List[str]:
		return open(input_path).read().strip().split("\n")

	@staticmethod
	def item_score(character):
		character_ord = ord(character)
		if ord('A') <= character_ord <= ord('Z'):
			return character_ord - ord('A') + 27
		if ord('a') <= character_ord <= ord('z'):
			return character_ord - ord('a') + 1
		raise ValueError()

	def question_1(self, input_path) -> int:
		sacks = self.parse(input_path)
		result = 0
		for sack in sacks:
			compartment_length = len(sack) // 2
			compartment1, compartment2 = sack[:compartment_length], sack[compartment_length:]
			common_item = set(compartment1).intersection(compartment2).pop()
			result += self.item_score(common_item)
		return result

	def question_2(self, input_path) -> int:
		sacks = self.parse(input_path)
		result = 0
		for sack1_index in range(0, len(sacks), 3):
			sack1, sack2, sack3 = sacks[sack1_index: sack1_index + 3]
			common_item = set(sack1).intersection(sack2).intersection(sack3).pop()
			result += self.item_score(common_item)
		return result


if __name__ == '__main__':
	Advent2022day3().run()
