from typing import Self, Any

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

    def __add__(self, other: Any) -> Self:
        if isinstance(other, Coord2D):
            return Coord2D(self.i + other.i, self.j + other.j)
        return NotImplemented

    def __sub__(self, other: Any) -> Self:
        if isinstance(other, Coord2D):
            return Coord2D(self.i - other.i, self.j - other.j)
        return NotImplemented

    def __iter__(self):
        return iter((self.i, self.j))


def neighbours(pos: Coord2D, grid: list = None, include_diag: bool = False) -> set[Coord2D]:
    directions = [Coord2D(1, 0), Coord2D(0, 1), Coord2D(-1, 0), Coord2D(0, -1)]
    possible_neighbours = [pos + direction for direction in directions]
    if include_diag:
        raise NotImplementedError()
    if grid:
        possible_neighbours = {n for n in possible_neighbours if in_grid(grid, n)}
    return possible_neighbours


if __name__ == '__main__':
    print(Coord2D(1, 0) + 2)
