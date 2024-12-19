from AbstractDailyProblem import AbstractDailyProblem
from utils import Coord2D

directions = {
	'v': Coord2D(1, 0),
	'^': Coord2D(-1, 0),
	'>': Coord2D(0, 1),
	'<': Coord2D(0, -1)
}


def attempt_move(warehouse, robot_pos: Coord2D, direction: Coord2D):
	# First, check if move is possible
	checked_pos = robot_pos
	while warehouse[checked_pos.i][checked_pos.j] != '#':
		if warehouse[checked_pos.i][checked_pos.j] == '.':
			break
		else:
			checked_pos += direction

	# If empty space is found, move boxes and robot
	if warehouse[checked_pos.i][checked_pos.j] != '#':
		# Translate optional boxes
		warehouse[checked_pos.i][checked_pos.j] = 'O'
		# Free robot pos
		warehouse[robot_pos.i][robot_pos.j] = '.'
		# Mark robot pos
		robot_pos += direction
		warehouse[robot_pos.i][robot_pos.j] = '@'

	return robot_pos


def can_move(warehouse, position: Coord2D, direction: Coord2D) -> bool:
	target = position + direction
	match warehouse[target.i][target.j]:
		case '.': return True
		case '#': return False
		case 'O': return can_move(warehouse, target, direction)
		# In the lines below, only propagate to the neighbour parenthesis if the box is pushed from above or from below
		case '[': return can_move(warehouse, target, direction) and (direction.j or can_move(warehouse, target + Coord2D(0, 1), direction))
		case ']': return can_move(warehouse, target, direction) and (direction.j or can_move(warehouse, target - Coord2D(0, 1), direction))
		case _: raise ValueError(f"What's that pokemon ? {target}")


def do_move(warehouse, position: Coord2D, direction: Coord2D, already_moved: set[Coord2D] = None) -> Coord2D:
	if already_moved is None:
		already_moved = set()

	target = position + direction

	if position not in already_moved:
		already_moved.add(position)

		match warehouse[target.i][target.j]:
			case '[':
				do_move(warehouse, target, direction, already_moved)
				do_move(warehouse, target + Coord2D(0, 1), direction, already_moved)
			case ']':
				do_move(warehouse, target, direction, already_moved)
				do_move(warehouse, target - Coord2D(0, 1), direction, already_moved)

		warehouse[target.i][target.j] = warehouse[position.i][position.j]
		warehouse[position.i][position.j] = '.'

	return target


def widen_warehouse(warehouse):
	extensions = {'#': '##', 'O': '[]', '.': '..', '@': '@.'}
	wide_warehouse = []
	for row in warehouse:
		wide_warehouse.append([])
		for c in row:
			wide_warehouse[-1].extend(extensions[c])
	return wide_warehouse


def print_warehouse(warehouse):
	print('\n'.join(''.join(l) for l in warehouse))


class Advent2024day15(AbstractDailyProblem):

	def parse(self, input_path: str, entry_separator='\n'):
		warehouse, trajectory = super().parse(input_path, '\n\n')
		return [list(line) for line in warehouse.split('\n')], trajectory.replace('\n', '')

	def __init__(self):
		super().__init__(10092, 9021)

	def question_2(self, input_path: str) -> int:
		warehouse, trajectory = self.parse(input_path)
		warehouse = widen_warehouse(warehouse)
		robot_pos = Coord2D(*next((i, j) for i in range(len(warehouse)) for j in range(len(warehouse[0])) if warehouse[i][j] == '@'))
		for move in trajectory:
			if can_move(warehouse, robot_pos, directions[move]):
				robot_pos = do_move(warehouse, robot_pos, directions[move])

		print_warehouse(warehouse)

		res = 0
		for i in range(len(warehouse)):
			for j in range(len(warehouse[0])):
				if warehouse[i][j] == '[':
					res += 100*i + j
		return res

	def question_1(self, input_path: str) -> int:
		warehouse, trajectory = self.parse(input_path)
		robot_pos = Coord2D(*next((i, j) for i in range(len(warehouse)) for j in range(len(warehouse[0])) if warehouse[i][j] == '@'))
		for move in trajectory:
			robot_pos = attempt_move(warehouse, robot_pos, directions[move])

		res = 0
		for i in range(len(warehouse)):
			for j in range(len(warehouse[0])):
				if warehouse[i][j] == 'O':
					res += 100*i + j
		return res


if __name__ == '__main__':
	Advent2024day15().run('../resources/2024/15/test.txt', '../resources/2024/15/input.txt')
