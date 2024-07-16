import cProfile

import networkx as nx

from AbstractDailyProblem import AbstractDailyProblem
from utils import display_grid, in_grid

cardinal_vectors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
slopes = {(0, 1): '>', (0, -1): '<', (1, 0): 'v', (-1, 0): '^'}


def longest_path_from(x, y, grid, prev_pos, overcome_slopes: bool) -> int:
	next_pos = [(x, y)]
	trail_length = 0
	while len(next_pos) == 1:
		x, y = next_pos[0]
		prev_pos.add(next_pos[0])
		trail_length += 1
		next_pos = [
			(x1, y1)
			for x1, y1 in [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]
			if in_grid(grid, (x1, y1)) and (x1, y1) not in prev_pos
			and (overcome_slopes or grid[x1][y1] not in {'#', slopes[x-x1, y-y1]})
		]
	if (x, y) == (len(grid) - 1, len(grid[0]) - 2):
		return trail_length - 1
	elif not next_pos:
		return -100000
	else:
		prev_pos = set(prev_pos)
		prev_pos.add((x, y))
		return trail_length + max(longest_path_from(x1, y1, grid, prev_pos.copy(), overcome_slopes) for x1, y1 in next_pos)


def recursive_longest_path_on_graph(current_node, destination, graph: nx.Graph, partial_path: set) -> int:
	if current_node == destination:
		return 0

	if destination in graph.neighbors(current_node):
		next_nodes = [destination]
	else:
		next_nodes = set(graph.neighbors(current_node)).difference(partial_path)

	if not next_nodes:
		return -100000
	else:
		partial_path = partial_path.union({current_node})
		return max(
			graph.get_edge_data(current_node, neighbour)['weight'] + recursive_longest_path_on_graph(neighbour, destination, graph, partial_path)
			for neighbour in next_nodes
		)


def build_graph(grid) -> nx.Graph:
	graph = nx.Graph()
	max_i, max_j = len(grid), len(grid[0])
	paths = {(i, j) for i in range(max_i) for j in range(max_j) if grid[i][j] != '#'}
	for x, y in paths:
		for di, dj in [(x, y+1), (x+1, y)]:
			if (di, dj) in paths:
				graph.add_edge((x, y), (di, dj), weight=1)

	for node in filter(lambda n: graph.degree[n] == 2, list(graph.nodes)):
		neighbors = list(graph.neighbors(node))
		graph.add_edge(*neighbors, weight=sum(graph.get_edge_data(node, neigh)['weight'] for neigh in neighbors))
		graph.remove_node(node)

	return graph


class Advent2023day23(AbstractDailyProblem):

	def __init__(self):
		super().__init__(94, 154)

	def question_1(self, input_path) -> int:
		grid = self.parse(input_path)
		return longest_path_from(0, 1, grid, set(), False)

	def question_2(self, input_path) -> int:
		grid = self.parse(input_path)
		graph = build_graph(grid)
		print(len(graph.nodes))
		return recursive_longest_path_on_graph((0, 1), (len(grid) - 1, len(grid[0]) - 2), graph, set())


if __name__ == '__main__':
	Advent2023day23().run('../resources/2023/23/test.txt', '../resources/2023/23/input.txt')
