def increases_in_list(iterator):
    prev_number = next(iterator)
    increases = 0
    for number in iterator:
        if number > prev_number:
            increases += 1
        prev_number = number
    return increases


def q1(path):
    return increases_in_list(int(_) for _ in open(path).readlines())


def q2(path):
    lines = [int(_) for _ in open(path).readlines()]
    triplets = zip(lines[:-2], lines[1:-1], lines[2:])
    return increases_in_list(map(sum, triplets))


if __name__ == '__main__':
    assert q1("test.txt") == 7
    print(q1("data.txt"))
    assert q2("test.txt") == 5
    print(q2("data.txt"))
