import numpy as np


def parse(path) -> np.ndarray:
    def process(e):
        return [int(_) for _ in e.strip()]
    return np.array(list(map(process, open(path).readlines())))


def neighbours(i, j, I, J):
    res = []
    if i > 0:
        res.append((i-1, j))
    if i < I - 1:
        res.append((i + 1, j))
    if j > 0:
        res.append((i, j - 1))
    if j < J - 1:
        res.append((i, j + 1))
    return res


def q1(path):
    height = parse(path)
    I, J = height.shape
    risk = height + 1

    def local_min_risk(i, j):
        return min(risk[_] for _ in neighbours(i, j, I, J))

    min_risk = np.array([[local_min_risk(i, j) for j in range(J)] for i in range(I)])
    return risk[risk < min_risk].sum()


def q2(path):
    from functools import reduce
    height = parse(path)
    I, J = height.shape
    risk = height + 1

    def local_min_risk(i, j):
        return min(risk[_] for _ in neighbours(i, j, I, J))

    min_risk = np.array([[local_min_risk(i, j) for j in range(J)] for i in range(I)])
    basin_sources = list(zip(*np.where(risk < min_risk)))

    basin_sizes = {source: 0 for source in basin_sources}
    points_to_explore = {(_, _) for _ in basin_sources}
    explored_points = set()

    while points_to_explore:
        point, source = points_to_explore.pop()
        explored_points.add(point)
        if height[point] < 9:
            basin_sizes[source] += 1
            points_to_explore.update((_, source) for _ in filter(lambda _: _ not in explored_points, neighbours(*point, I, J)))

    top_basin_sizes = sorted(basin_sizes.values(), reverse=True)[:3]
    return reduce((lambda x, y: x * y), top_basin_sizes)


if __name__ == '__main__':
    assert q1("test.txt") == 15
    print(q1("data.txt"))
    assert q2("test.txt") == 1134
    print(q2("data.txt"))
