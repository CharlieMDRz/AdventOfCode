from typing import Self

import attrs as attrs


def in_grid(grid, pos):
    i, j, *_ = pos
    return 0 <= i < len(grid) and 0 <= j < len(grid[0])


def display_grid(grid) -> None:
    print(
        '\n'.join([''.join(map(str, _)) for _ in grid])
    )


@attrs.define(frozen=True)
class IntCoord:
    i: int
    j: int

    def __add__(self, other) -> Self:
        if isinstance(other, IntCoord):
            return IntCoord(self.i + other.i, self.j + other.j)
        return NotImplemented("IntCoord can only be added to instances of the same class")

    def __sub__(self, other) -> Self:
        if isinstance(other, IntCoord):
            return IntCoord(self.i - other.i, self.j - other.j)
        return NotImplemented("IntCoord can only be subtracted to instances of the same class")

    def __iter__(self):
        return iter((self.i, self.j))


def neighbours(pos: IntCoord, grid, include_diag = False) -> set[IntCoord]:
    directions = [IntCoord(1, 0), IntCoord(0, 1), IntCoord(-1, 0), IntCoord(0, -1)]
    possible_neighbours = [pos + direction for direction in directions]
    if include_diag:
        raise NotImplementedError()
    return {n for n in possible_neighbours if in_grid(grid, n)}
