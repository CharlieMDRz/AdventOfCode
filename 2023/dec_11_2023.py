from AbstractDailyProblem import AbstractDailyProblem


def distance(xy1: tuple[int, int], xy2: tuple[int, int]) -> int:
    """absolute distance between two galaxies (number of steps from on to another)"""
    x1, y1 = xy1
    x2, y2 = xy2
    return abs(x2 - x1) + abs(y2 - y1)


def galaxies_distance(galaxies: list[tuple[int, int]]) -> int:
    """
    Sum of distance between pairs of galaxies
    Galaxies (coord tuples) are indexed to simplify the computation
    """
    indexed_galaxies = {g: index for index, g in enumerate(galaxies)}
    return sum(
        distance(g1, g2) for g1 in galaxies for g2 in galaxies if indexed_galaxies[g1] < indexed_galaxies[g2]
    )


def expand(galaxies: list[tuple[int, int]], spread: int = 2):
    """Expand the universe by given pad"""
    # row spreading: translate all galaxies with x > spread row
    row_index = 0
    while row_index < max(_[0] for _ in galaxies):
        if any(_[0] == row_index for _ in galaxies):
            row_index += 1
        else:
            for index, (x, y) in enumerate(galaxies):
                if x > row_index:
                    galaxies[index] = (x+spread-1, y)
            row_index += spread
    # col spreading: translate all galaxies with y > spread column
    col_index = 0
    while col_index < max(_[1] for _ in galaxies):
        if any(_[1] == col_index for _ in galaxies):
            col_index += 1
        else:
            for index, (x, y) in enumerate(galaxies):
                if y > col_index:
                    galaxies[index] = (x, y+spread-1)
            col_index += spread
    return galaxies


def display(galaxies: list[tuple[int, int]]):
    n_rows = max(g[0] for g in galaxies) + 1
    n_cols = max(g[1] for g in galaxies) + 1
    data = [['.' for _ in range(n_cols)] for _ in range(n_rows)]
    for x, y in galaxies:
        data[x][y] = '#'
    print('\n'.join(map(''.join, data)))


class Advent2023day11(AbstractDailyProblem):
    """2023-12-11"""

    def __init__(self) -> None:
        super().__init__(374, 0)

    def parse(self, input_path: str, entry_separator='\n') -> list[tuple[int, int]]:
        galaxies_pos = []
        raw_data = super().parse(input_path, entry_separator)
        for row_index, row in enumerate(raw_data):
            for col_index, value in enumerate(row):
                if value == '#':
                    galaxies_pos.append((row_index, col_index))
        return galaxies_pos

    def question_1(self, input_path) -> int:
        galaxies = self.parse(input_path)
        expand(galaxies)
        return galaxies_distance(galaxies)

    def question_2(self, input_path) -> int:
        galaxies = self.parse(input_path)
        if 'test' in input_path:
            expand(galaxies, 10)
            assert galaxies_distance(galaxies) == 1030
            expand(galaxies, 10)
            assert galaxies_distance(galaxies) == 8410
            return 0
        else:
            expand(galaxies, 1000000)
            return galaxies_distance(galaxies)


if __name__ == '__main__':
    Advent2023day11().run('../resources/2023/11/test.txt', '../resources/2023/11/input.txt')
