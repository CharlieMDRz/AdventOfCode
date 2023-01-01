import functools
import re
from typing import Dict, List

from AbstractDailyProblem import AbstractDailyProblem


Blueprint = Dict[str, Dict[str, int]]

blueprints: List[Blueprint]


def can_afford(recipe, c_o, c_c, c_ob, c_g):
	if c_o < recipe['ore']:
		return False
	if c_c < recipe['clay']:
		return False
	if c_ob < recipe['obsidian']:
		return False
	if c_g < recipe['geode']:
		return False
	return True


@functools.lru_cache()
def quality_level(bp, s, r_o, c_o, r_c, c_c, r_ob, c_ob, r_g, c_g):
	if s == 0:
		return c_g  # never reached
	elif s == 1:
		return c_g + r_g

	possible_next_states = [(bp, s-1, r_o, c_o + r_o, r_c, c_c + r_c, r_ob, c_ob + r_ob, r_g, c_g + r_g)]
	affordable_robots = [robot for robot, recipe in blueprints[bp].items() if can_afford(recipe, c_o, c_c, c_ob, c_g)]
	if 'geode' in affordable_robots: affordable_robots = ['geode']  # heuristic: build 'em asap
	for robot in affordable_robots:
		recipe = blueprints[bp][robot]
		couldnt_prev_round = not can_afford(recipe, c_o - r_o, c_c - r_c, c_ob - r_ob, c_g - r_g)
		useful_new_robot = {'ore': r_o, 'obsidian': r_ob, 'clay': r_c, 'geode': -1}[robot] < max(recipe[robot] for recipe in blueprints[bp].values())
		if couldnt_prev_round and useful_new_robot:
			possible_next_states.append((
				bp, s-1,
				r_o + int(robot == 'ore'), c_o + r_o - recipe['ore'],
				r_c + int(robot == 'clay'), c_c + r_c - recipe['clay'],
				r_ob + int(robot == 'obsidian'), c_ob + r_ob - recipe['obsidian'],
				r_g + int(robot == 'geode'), c_g + r_g - recipe['geode'],
			))
	return max(quality_level(*next_state) for next_state in possible_next_states)


class Advent2022day19(AbstractDailyProblem):

	def parse(self, input_path, entry_separator='\n'):
		return super().parse(input_path, 'Blueprint')[1:]

	def parse_entry(self, entry: str) -> Blueprint:
		robot_costs_str = entry.strip().split('Each')[1:]
		blueprint = {}
		for robot_recipe_str in robot_costs_str:  # type: str
			robot_type = robot_recipe_str.strip().split()[0]
			robot_recipe = {resource: 0 for resource in ['ore', 'clay', 'obsidian', 'geode']}
			for count, resource in re.findall("(\d+) (\w+)", robot_recipe_str):
				robot_recipe[resource] = int(count)
			blueprint[robot_type] = robot_recipe
		return blueprint

	def question_1(self, input_path) -> int:
		global blueprints
		blueprints = self.parse(input_path)
		res = 0
		for index, bp in enumerate(blueprints):
			res += quality_level(index, 24, 1, 0, 0, 0, 0, 0, 0, 0) * (index + 1)
		return res

	def question_2(self, input_path) -> int:
		global blueprints
		blueprints = self.parse(input_path)[:3]
		res = 1
		for index, bp in enumerate(blueprints):
			score = quality_level(index, 32, 1, 0, 0, 0, 0, 0, 0, 0)
			res *= score
		return res

	def __init__(self):
		super().__init__(33, 3472)


if __name__ == '__main__':
	Advent2022day19().run('../resources/2022/19/test.txt', '../resources/2022/19/input.txt')
