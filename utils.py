def in_grid(grid, pos):
    i, j, *_ = pos
    return 0 <= i < len(grid) and 0 <= j < len(grid[0])


def display_grid(grid) -> None:
    print(
        '\n'.join([''.join(map(str, _)) for _ in grid])
    )

