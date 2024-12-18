import networkx as nx

from AbstractDailyProblem import AbstractDailyProblem


class Advent2024day18(AbstractDailyProblem):

	def __init__(self):
		super().__init__(22, '6,1')

	def parse_entry(self, entry: str):
		return tuple(map(int, entry.strip().split(',')))

	def question_1(self, input_path) -> int:
		falling_bytes = self.parse(input_path)
		grid_dim = 7 if 'test' in input_path else 71
		byte_count = 12 if 'test' in input_path else 1024
		grid: nx.Graph = nx.grid_2d_graph(grid_dim, grid_dim)

		for byte_id in range(byte_count):
			i, j = falling_bytes[byte_id]
			grid.remove_node((i, j))

		return nx.shortest_path_length(grid, (0, 0), (grid_dim-1, grid_dim-1))

	def question_2(self, input_path) -> str:
		falling_bytes = self.parse(input_path)
		grid_dim = 7 if 'test' in input_path else 71
		byte_count = 12 if 'test' in input_path else 1024
		grid: nx.Graph = nx.grid_2d_graph(grid_dim, grid_dim)

		# From q1, we know that these bytes are not blocking
		for byte_id in range(byte_count):
			i, j = falling_bytes[byte_id]
			grid.remove_node((i, j))

		path = None
		for byte_id in range(byte_count, len(falling_bytes)):
			i, j = falling_bytes[byte_id]
			grid.remove_node((i, j))
			# No need to recompute path if new byte does not obstruct previous known path
			if not path or (i, j) in path:
				try:
					path = set(nx.shortest_path(grid, (0, 0), (grid_dim-1, grid_dim-1)))
				except nx.NetworkXNoPath:
					return f'{i},{j}'


if __name__ == '__main__':
	Advent2024day18().run('../resources/2024/18/test.txt', '../resources/2024/18/input.txt')
