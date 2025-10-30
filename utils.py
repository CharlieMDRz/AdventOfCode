from typing import Self, Any, Iterable

import attrs as attrs


def in_grid(grid, pos):
    i, j, *_ = pos
    return 0 <= i < len(grid) and 0 <= j < len(grid[0])


def display_grid(grid) -> None:
    print(
        '\n'.join([''.join(map(str, _)) for _ in grid])
    )


@attrs.define(frozen=True)
class Coord2D:
    i: float
    j: float

    def rotate(self) -> Self:
        return Coord2D(-self.j, self.i)

    @property
    def manhattan(self) -> float:
        return abs(self.i) + abs(self.j)

    def __add__(self, other: Any) -> Self:
        if isinstance(other, Coord2D):
            return Coord2D(self.i + other.i, self.j + other.j)
        return NotImplemented

    def __sub__(self, other: Any) -> Self:
        if isinstance(other, Coord2D):
            return Coord2D(self.i - other.i, self.j - other.j)
        return NotImplemented

    def __mul__(self, other) -> Self:
        return Coord2D(self.i * other, self.j * other)

    def __iter__(self):
        return iter((self.i, self.j))

    @classmethod
    def from_dir(cls, direction: str) -> Self:
        return {
            'U': cls(-1, 0),
            'D': cls(1, 0),
            'L': cls(0, -1),
            'R': cls(0, 1),
        }[direction]


Segment = tuple[Coord2D, Coord2D]

def get_directions(include_diag: bool = False) -> Iterable[Coord2D]:
    if include_diag:
        raise NotImplementedError()
    else:
        return [Coord2D(1, 0), Coord2D(0, 1), Coord2D(-1, 0), Coord2D(0, -1)]

def neighbours(pos: Coord2D, grid: list = None, include_diag: bool = False) -> set[Coord2D]:
    directions = get_directions(include_diag)
    possible_neighbours = [pos + direction for direction in directions]
    if include_diag:
        raise NotImplementedError()
    if grid:
        possible_neighbours = {n for n in possible_neighbours if in_grid(grid, n)}
    return possible_neighbours


if __name__ == '__main__':
    print(Coord2D(1, 0) + 2)
