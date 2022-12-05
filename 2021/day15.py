import itertools
from typing import Tuple, List, Iterable

import numpy as np

Point = Tuple[int, int]
Path = List[Point]


class Dijkstra:
    def __init__(self, cost_matrix):
        print(cost_matrix.shape)
        self.cost = cost_matrix

    def neighbours(self, position: Point) -> Iterable[Point]:
        x, y = position
        if x > 0:
            yield x-1, y
        if x < self.cost.shape[0] - 1:
            yield x+1, y
        if y > 0:
            yield x, y-1
        if y < self.cost.shape[1] - 1:
            yield x, y+1

    def get_distance(self, source: Point, dest: Point) -> int:
        position = source
        explored_positions = set()
        positions_to_explore = set()
        distance_map = np.full(self.cost.shape, 100000000)
        distance_map[source] = 0

        while position != dest:
            for neighbour in self.neighbours(position):
                if neighbour not in explored_positions:
                    distance_map[neighbour] = min(distance_map[neighbour], distance_map[position] + self.cost[neighbour])
                    positions_to_explore.add(neighbour)

            explored_positions.add(position)
            position = min(positions_to_explore, key=distance_map.__getitem__)
            positions_to_explore.remove(position)
        return distance_map[dest]


def parse(input_path: str) -> np.ndarray:
    matrix_lines = []
    for line in open(input_path).read().split('\n'):
        matrix_lines.append([int(char) for char in line])

    return np.array(matrix_lines)


def q1(path):
    cost_matrix = parse(path)
    dijkstra = Dijkstra(cost_matrix)
    origin = (0, 0)
    destination = (cost_matrix.shape[0] - 1, cost_matrix.shape[1] - 1)
    return dijkstra.get_distance(origin, destination)


def q2(path):
    tile_cost_matrix = parse(path)
    width, length = tile_cost_matrix.shape
    cost_matrix = np.zeros((width * 5, length * 5), dtype=int)

    for tile_x, tile_y in itertools.product(range(5), range(5)):
        sub_cost_matrix = (tile_cost_matrix + tile_x + tile_y - 1) % 9 + 1
        cost_matrix[tile_x * width: (tile_x+1) * width, tile_y * length: (tile_y+1) * length] = sub_cost_matrix
    dijkstra = Dijkstra(cost_matrix)
    origin = (0, 0)
    destination = (cost_matrix.shape[0] - 1, cost_matrix.shape[1] - 1)
    return dijkstra.get_distance(origin, destination)


if __name__ == '__main__':
    print(parse('../resources/2021/15/test.txt'))
    assert q1('../resources/2021/15/test.txt') == 40
    assert q2('../resources/2021/15/test.txt') == 315
    print(f"Q1 answer: {q1('../resources/2021/15/data.txt')}")
    print(f"Q2 answer: {q2('../resources/2021/15/data.txt')}")
