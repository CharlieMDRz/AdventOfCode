from AbstractDailyProblem import AbstractDailyProblem
from utils import Coord2D


def get_positions(wire: list[tuple[str, int]]) -> dict[Coord2D, int]:
	positions = {}
	segment_start = Coord2D(0, 0)
	distance = 0
	for wire_dir, wire_length in wire:
		wire_vec = Coord2D.from_dir(wire_dir)
		positions.update({(segment_start + wire_vec * i): (distance + i) for i in range(wire_length)})

		segment_start = segment_start + wire_vec * wire_length
		distance += wire_length
	return positions


class Advent2019day3(AbstractDailyProblem):

	def __init__(self) -> None:
		super().__init__(159, 610)

	def parse_entry(self, entry: str):
		return [(e[0], int(e[1:])) for e in entry.split(',')]

	def question_1(self, input_path: str) -> float:
		wires = self.parse(input_path)
		wire1, wire2 = map(get_positions, wires)
		intersections: set[Coord2D] = set(wire1.keys()).intersection(wire2.keys())
		intersections.remove(Coord2D(0, 0))
		return min(i.manhattan for i in intersections)

	def question_2(self, input_path: str) -> int:
		wires = self.parse(input_path)
		wire1, wire2 = map(get_positions, wires)
		intersections: set[Coord2D] = set(wire1.keys()).intersection(wire2.keys())
		intersections.remove(Coord2D(0, 0))

		return min(wire1[i] + wire2[i] for i in intersections)


if __name__ == '__main__':
	Advent2019day3().run('../resources/2019/3/test.txt', '../resources/2019/3/input.txt')
