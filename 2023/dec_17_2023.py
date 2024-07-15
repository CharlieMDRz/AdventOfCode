import functools

from AbstractDailyProblem import AbstractDailyProblem
from sortedcontainers.sortedlist import SortedList
from utils import in_grid



def get_predecessor_path(predecessor_map, node):
	predecessor_path = [node]
	while (tail := predecessor_path[-1]) in predecessor_map:
		predecessor_path.append(predecessor_map[tail])
	return reversed(predecessor_path)


def a_star(grid, sx, sy, tx, ty, min_with_turn, max_without_turn):
	source_node = sx, sy, 1, 0, -1
	cost = {source_node: grid[sx][sy]}
	heuristic = {source_node: cost[source_node] + abs(tx - sx) + abs(ty - sy)}
	predecessor = {}
	to_explore = SortedList([source_node], key=heuristic.get)
	to_explore_set = {source_node}
	explored = set()
	while to_explore:
		node = x, y, dx, dy, steps = to_explore.pop(0)
		explored.add(node)
		if (x, y) == (tx, ty):
			return get_predecessor_path(predecessor, node)
		else:
			if (x or y) and steps < min_with_turn:
				moves = [(dx, dy)]
			elif steps < max_without_turn:
				moves = [(dx, dy), (dy, dx), (-dy, -dx)]
			else:
				moves = [(dy, dx), (-dy, -dx)]

			for new_dx, new_dy in moves:
				next_node = x+new_dx, y+new_dy, new_dx, new_dy, steps + 1 if (dx, dy) == (new_dx, new_dy) else 1
				if not in_grid(grid, next_node):
					continue

				next_node_cost = cost[node] + grid[next_node[0]][next_node[1]]
				if (
					next_node not in explored
					and (next_node not in to_explore_set or next_node_cost < cost[next_node])
				):
					predecessor[next_node] = node
					cost[next_node] = next_node_cost
					heuristic[next_node] = cost[next_node] + abs(tx - next_node[0]) + abs(ty - next_node[1])
					to_explore.add(next_node)
					to_explore_set.add(next_node)

	return ValueError("Path finding failed")


def display(grid, path):
	disp = [[str(cell) for cell in row] for row in grid]
	char = {
		(1, 0): 'v',
		(-1, 0): '^',
		(0, 1): '>',
		(0, -1): '<'
	}
	for x, y, dx, dy, _ in path[1:]:
		disp[x][y] = char[(dx, dy)]

	print('\n'.join([''.join(_) for _ in disp]))


class Advent2023day17(AbstractDailyProblem):

	def question_1(self, input_path) -> int:
		grid = self.parse(input_path)
		shortest_path = list(a_star(grid, 0, 0, len(grid) - 1, len(grid[0]) - 1, 0, 3))
		display(grid, shortest_path)
		return sum([
			grid[x][y] for x, y, *_ in shortest_path[1:]
		])

	def question_2(self, input_path) -> int:
		grid = self.parse(input_path)
		shortest_path = list(a_star(grid, 0, 0, len(grid) - 1, len(grid[0]) - 1, 4, 10))
		# display(grid, shortest_path)
		return sum([
			grid[x][y] for x, y, *_ in shortest_path[1:]
		])

	def __init__(self):
		super().__init__(102, 94)

	def parse_entry(self, entry: str):
		return list(map(int, entry))


if __name__ == '__main__':
	Advent2023day17().run('../resources/2023/17/test.txt', '../resources/2023/17/input.txt')
