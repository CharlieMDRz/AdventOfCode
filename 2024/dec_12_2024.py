import itertools

import networkx as nx

from AbstractDailyProblem import AbstractDailyProblem
from utils import Coord2D, neighbours


def get_gardens(crops) -> list[set[Coord2D]]:
	# Create adjacency graph: crops are connected if they are adjacent and of same type
	garden_graph = nx.Graph()
	for i, j in itertools.product(range(len(crops)), range(len(crops[0]))):
		crop_pos = Coord2D(i, j)
		garden_graph.add_node(crop_pos)
		for crop_neighbour in neighbours(crop_pos, crops):
			if crops[i][j] == crops[crop_neighbour.i][crop_neighbour.j]:
				garden_graph.add_edge(crop_pos, crop_neighbour)

	return list(nx.connected_components(garden_graph))


def garden_perimeter(garden_crops: set[Coord2D]) -> int:
	perimeter = 0
	for crop_pos in garden_crops:
		for neighbour_pos in neighbours(crop_pos):
			if neighbour_pos not in garden_crops:
				perimeter += 1
	return perimeter


def garden_sides(garden_crops: set[Coord2D]) -> int:
	fence_coords = set()
	for crop_pos in garden_crops:
		for neighbour_pos in neighbours(crop_pos):
			if neighbour_pos not in garden_crops:
				fence_coords.add(Coord2D((crop_pos.i+neighbour_pos.i)/2, (crop_pos.j+neighbour_pos.j)/2))

	fence_graph = nx.Graph()
	for fence in fence_coords:
		fence_graph.add_node(fence)
		fence_neighbours = {fence + Coord2D(-1, 0), fence + Coord2D(1, 0)} if fence.i%1 == 0 else {fence + Coord2D(0, -1), fence + Coord2D(0, 1)}
		for n in fence_neighbours.intersection(fence_coords):
			# Ugly edge case for crossings in the fences -> detects a T shape in the fences to break adjacency
			if Coord2D(min(fence.i, n.i) + .5, min(fence.j, n.j) + .5) not in fence_coords:
				fence_graph.add_edge(fence, n)
	return len(list(nx.connected_components(fence_graph)))


class Advent2024day12(AbstractDailyProblem):

	def __init__(self):
		super().__init__(1930, 1206)

	def question_1(self, input_path) -> int:
		crops = self.parse(input_path)
		gardens = get_gardens(crops)
		return sum(garden_perimeter(g) * len(g) for g in gardens)

	def question_2(self, input_path) -> int:
		crops = self.parse(input_path)
		gardens = get_gardens(crops)
		return sum(garden_sides(g) * len(g) for g in gardens)


if __name__ == '__main__':
	Advent2024day12().run('../resources/2024/12/test.txt', '../resources/2024/12/input.txt')
