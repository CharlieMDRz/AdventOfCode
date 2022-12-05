import math
import re
from collections import namedtuple
from typing import List, Tuple

from AbstractDailyProblem import AbstractDailyProblem

Stacks = List[List[str]]
StackMove = namedtuple('StackMove', ['source', 'target', 'iterations'])


class Advent2022day5(AbstractDailyProblem):

	def parse(self, input_path, entry_separator='\n') -> Tuple[Stacks, List[StackMove]]:
		data = open(input_path).read()
		stacks_data, moves_data = data.split("\n\n")
		return self.parse_stacks(stacks_data), self.parse_moves(moves_data.strip())

	@staticmethod
	def apply_move(stacks: Stacks, move: StackMove, reverse):
		moved_items = []
		for _ in range(move.iterations):
			moved_items.append(stacks[move.source].pop(-1))
		if not reverse:
			moved_items = reversed(moved_items)
		stacks[move.target].extend(moved_items)

	def question_1(self, input_path) -> str:
		stacks, moves = self.parse(input_path)
		for move in moves:
			self.apply_move(stacks, move, reverse=True)
		return ''.join(stack[-1] for stack in stacks[1:])

	def question_2(self, input_path) -> str:
		stacks, moves = self.parse(input_path)
		for move in moves:
			self.apply_move(stacks, move, reverse=False)
		return ''.join(stack[-1] for stack in stacks[1:])

	def __init__(self):
		super().__init__('CMZ', 'MCD')

	@staticmethod
	def parse_stacks(stacks_data: str):
		stacks_entries = reversed(stacks_data.split('\n'))
		stack_header = next(stacks_entries)
		stack_count = math.ceil(len(stack_header) / 4)
		stacks = [[] for _ in range(stack_count + 1)]
		for stack_entry in stacks_entries:
			for stack_id in range(math.ceil(len(stack_entry)/4)):
				stack_item = stack_entry[4 * stack_id + 1]
				if stack_item.strip():
					stacks[stack_id + 1].append(stack_item)
		return stacks

	@staticmethod
	def parse_moves(moves_data):
		pattern = re.compile("move (\\d+) from (\\d+) to (\\d+)")
		moves = []
		for move_data in moves_data.split("\n"):
			count, from_stack, to_stack = map(int, pattern.match(move_data).groups())
			moves.append(StackMove(from_stack, to_stack, count))
		return moves


if __name__ == '__main__':
	Advent2022day5().run("../resources/2022/5/test.txt", "../resources/2022/5/input.txt")
