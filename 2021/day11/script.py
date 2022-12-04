import numpy as np
from itertools import product


def process_line(e: str):
    return [int(_) for _ in e.strip()]


def parse(path: str):
    path = str(__file__) + '/../' + path
    return np.array(list(map(process_line, open(path).readlines())))


def step(data: np.ndarray):
    flashes = 0
    data += 1
    while data.max() > 9:
        for i, j in zip(*np.where(data > 9)):
            # Count flash
            flashes += 1
            data[i, j] = 0
            # Propagate to neighbours
            for i2, j2 in product(range(max(0, i-1), i+2), range(max(0, j-1), j+2)):
                try:
                    if data[i2, j2]:
                        data[i2, j2] += 1
                except IndexError:
                    continue  # out of bounds neighbours
    return flashes


def question1(path: str) -> int:
    data = parse(path)
    return sum(step(data) for _ in range(100))


def question2(path: str) -> int:
    data: np.ndarray = parse(path)
    return next(i for i in range(1, 2<<16) if step(data) == data.size)


if __name__ == "__main__":
    assert question1('test.txt') == 1656
    print("Answer #1: ", question1('input.txt'))
    assert question2('test.txt') == 195
    print("Answer #2: ", question2('input.txt'))
