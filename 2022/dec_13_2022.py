import functools
import json
from typing import List

from AbstractDailyProblem import AbstractDailyProblem


def int_in_right_order(left, right):
	if in_right_order(left, right):
		return -1
	return 1


def in_right_order(left, right):
	if type(left) is int and type(right) is int:
		return None if left == right else left < right
	elif type(left) is list and type(right) is list:
		return lists_in_right_order(left, right)
	elif type(left) is int:
		return in_right_order([left], right)
	else:
		return in_right_order(left, [right])


def lists_in_right_order(left: List, right: List):
	for left_item, right_item in zip(left, right):
		comp_left_right = in_right_order(left_item, right_item)
		if comp_left_right is not None:
			return comp_left_right
	if len(left) != len(right):
		return len(left) < len(right)
	else:
		return None


class Advent2022day13(AbstractDailyProblem):

	def parse(self, input_path, entry_separator='\n'):
		return super().parse(input_path, '\n\n')

	def parse_entry(self, entry):
		return tuple(json.loads(_) for _ in entry.split('\n'))

	def question_1(self, input_path) -> int:
		entries = self.parse(input_path)
		return sum((_+1) for _ in range(len(entries)) if in_right_order(*entries[_]))

	def question_2(self, input_path) -> int:
		raw_entries = self.parse(input_path)
		entries = [packet for packet_pair in raw_entries for packet in packet_pair] + [[2], [6]]
		sorted_entries = sorted(entries, key=functools.cmp_to_key(int_in_right_order))
		return (sorted_entries.index([2]) + 1) * (sorted_entries.index([6]) + 1)

	def __init__(self):
		super().__init__(13, 140)


if __name__ == '__main__':
	Advent2022day13().run('../resources/2022/13/test.txt', '../resources/2022/13/input.txt')
