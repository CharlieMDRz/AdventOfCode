import itertools

import networkx as nx

from AbstractDailyProblem import AbstractDailyProblem
from utils import Coord2D, neighbours, get_directions


def maze_to_graph(maze: list[str]) -> nx.Graph:
	maze_graph = nx.Graph()
	for row_id, col_id in itertools.product(range(len(maze)), range(len(maze[0]))):
		if maze[row_id][col_id] == '#':
			continue
		position = Coord2D(row_id, col_id)
		neighbourhood = [n for n in neighbours(position, maze) if maze[n.i][n.j] != '#']
		if maze[row_id][col_id] != '.' or len(neighbourhood) > 2 or len(neighbourhood) == 2 and 0 not in neighbourhood[0]-neighbourhood[1]:
			for direction in get_directions():
				maze_graph.add_edge((position, direction), (position, direction.rotate()), weight=1000)
		for neighbour in neighbourhood:
			direction = neighbour - position
			maze_graph.add_edge((position, direction), (neighbour, direction), weight=1)

	# Agregation of corridors
	for node in list(maze_graph.nodes):
		if maze[node[0].i][node[0].j] == '.' and len(list(maze_graph.neighbors(node))) == 2:
			n1, n2 = maze_graph.neighbors(node)
			maze_graph.add_edge(n1, n2, weight=sum(maze_graph.edges[node, n]['weight'] for n in (n1, n2)))
			maze_graph.remove_node(node)

	return maze_graph


class Advent2024day16(AbstractDailyProblem):

	def __init__(self):
		super().__init__(11048, 64)

	def question_1(self, input_path) -> int:
		maze = self.parse(input_path)
		graph = maze_to_graph(maze)
		source = (Coord2D(len(maze) - 2, 1), Coord2D(0, 1))
		target = Coord2D(1, len(maze[0]) - 2)
		return min(
			nx.shortest_path_length(graph, source, (target, d), weight='weight')
			for d in get_directions()
			if (target, d) in graph
		)

	def question_2(self, input_path) -> int:
		maze = self.parse(input_path)
		graph = maze_to_graph(maze)
		source = (Coord2D(len(maze) - 2, 1), Coord2D(0, 1))
		target = Coord2D(1, len(maze[0]) - 2)
		target_dir = min(get_directions(), key=lambda d: nx.shortest_path_length(graph, source, (target, d), weight="weight"))
		paths = nx.shortest_simple_paths(graph, source, (target, target_dir), weight='weight')
		pos_in_best_path = set()
		for path in paths:
			pos_in_best_path.update({node[0] for node in path})
		return len(pos_in_best_path)


if __name__ == '__main__':
	Advent2024day16().run('../resources/2024/16/test.txt', '../resources/2024/16/input.txt')
