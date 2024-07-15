from AbstractDailyProblem import AbstractDailyProblem
from utils import in_grid


def get_next_positions(grid, i, j, di, dj):
    try:
        grid_case = grid[i][j]
    except IndexError:
        return []

    match grid_case:
        case '.':
            return [(i + di, j + dj, di, dj)]
        case '/':
            di, dj = -dj, -di
            return [(i + di, j + dj, di, dj)]
        case '\\':
            di, dj = dj, di
            return [(i + di, j + dj, di, dj)]
        case '-':
            if di == 0:
                return [(i, j + dj, 0, dj)]
            else:
                return [(i, j + dj, 0, dj) for dj in (-1, 1)]
        case '|':
            if dj == 0:
                return [(i + di, j, di, 0)]
            else:
                return [(i + di, j, di, 0) for di in (-1, 1)]
        case _:
            raise NotImplementedError(f"{grid_case}")


def display(grid, explored):
    displayed_grid = [['.' for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for i, j, *_ in explored:
        try:
            displayed_grid[i][j] = '#'
        except IndexError:
            continue
    print('\n'.join([''.join(_) for _ in displayed_grid]))


def energize_from(grid, start):
    to_explore = [start]
    explored = set()
    while to_explore:
        point_and_direction = to_explore.pop(0)
        if point_and_direction not in explored:
            to_explore.extend(_ for _ in get_next_positions(grid, *point_and_direction) if in_grid(grid, _))
            explored.add(point_and_direction)

    return {(i, j) for i, j, *_ in explored}


class Advent2023day16(AbstractDailyProblem):

    def question_1(self, input_path) -> int:
        grid = self.parse(input_path)
        return len(energize_from(grid, (0, 0, 0, 1)))

    def parse_entry(self, entry: str):
        return list(super().parse_entry(entry))

    def question_2(self, input_path) -> int:
        grid = self.parse(input_path)
        height, width = len(grid), len(grid[0])
        starts = [(0, j, 1, 0) for j in range(width)] + [(height - 1, j, -1, 0) for j in range(width)] \
            + [(i, 0, 0, 1) for i in range(height)] + [(i, width - 1, 0, -1) for i in range(height)]

        return max([len(energize_from(grid, start)) for start in starts])

    def __init__(self) -> None:
        super().__init__(46, 51)


if __name__ == '__main__':
    Advent2023day16().run('../resources/2023/16/test.txt', '../resources/2023/16/input.txt')
