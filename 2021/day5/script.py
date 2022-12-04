import numpy as np

def process_line(e: str):
    p1, p2 = e.split(' -> ')
    coords = (*p1.split(','), *p2.split(','))
    return [int(_) for _ in coords]


def parse(path: str):
    path = str(__file__) + '/../' + path
    return list(map(process_line, open(path).readlines()))


def question1(path: str) -> int:
    segments = parse(path)
    width = max(max(_[1], _[3]) for _ in segments) + 1
    height = max(max(_[0], _[2]) for _ in segments) + 1
    floor = np.zeros((width, height))
    for x1, y1, x2, y2 in segments:
        if (x1 > x2): x1, x2 = x2, x1
        if (y1 > y2): y1, y2 = y2, y1
        if (y2 - y1) * (x2 - x1) == 0:
            floor[x1:(x2+1), y1:(y2+1)] += 1
    return (floor > 1).sum()


def question2(path: str) -> int:
    segments = parse(path)
    width = max(max(_[1], _[3]) for _ in segments) + 1
    height = max(max(_[0], _[2]) for _ in segments) + 1
    floor = np.zeros((width, height))
    for x1, y1, x2, y2 in segments:
        if (y2 - y1) * (x2 - x1) == 0:
            if (x1 > x2): x1, x2 = x2, x1
            if (y1 > y2): y1, y2 = y2, y1
            floor[x1:(x2+1), y1:(y2+1)] += 1
        else:
            for x, y in zip(list(range(x1, x2, 1 if x1 <= x2 else -1)) + [x2], list(range(y1, y2, 1 if y1 <= y2 else -1)) + [y2]):
                floor[x, y] += 1
            del x, y
    return (floor > 1).sum()


if __name__ == "__main__":
    assert question1('test.txt') == 5
    print("Answer #1: ", question1('input.txt'))
    assert question2('test.txt') == 12
    print("Answer #2: ", question2('input.txt'))
