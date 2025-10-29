import math
import re

from AbstractDailyProblem import AbstractDailyProblem
from utils import Coord2D

MAX_INT = 1<<32

def min_cost_to_get_to_target_q1(a_button: Coord2D, b_button: Coord2D, a_cost: int, b_cost: int, prize: Coord2D, max_pushes=100) -> int:
	min_cost = MAX_INT
	for a_pushes in range(max_pushes + 1):
		cost = a_cost * a_pushes
		remainder = prize - a_button * a_pushes
		if (remainder.i % b_button.i == 0) and (remainder.j % b_button.j) == 0 and (remainder.i // b_button.i == remainder.j // b_button.j):
			cost += b_cost * (remainder.i // b_button.i)
			min_cost = min(min_cost, cost)

	if min_cost == MAX_INT:
		return False
	else:
		return min_cost


def min_cost_to_get_to_target_q2(a: Coord2D, b: Coord2D, p: Coord2D, a_cost: int = 3, b_cost: int = 1) -> int:
	x_div = math.gcd()


class Advent2024day13(AbstractDailyProblem):

	def __init__(self):
		super().__init__(480, 0)

	def parse_entry(self, entry: str):
		pattern = re.compile(r'\d+')
		return list(
			map(
				lambda l: Coord2D(*map(int, pattern.findall(l))),
				entry.strip().split('\n')
			)
		)

	def question_1(self, input_path) -> int:
		machines = self.parse(input_path, '\n\n')
		return sum(min_cost_to_get_to_target_q1(a, b, 3, 1, prize) for a, b, prize in machines)

	def question_2(self, input_path) -> int:
		pass


if __name__ == '__main__':
	Advent2024day13().run('../resources/2024/13/test.txt', '../resources/2024/13/input.txt')
