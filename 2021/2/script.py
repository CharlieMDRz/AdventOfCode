def parse(path):
    def process(e):
        cmd, dist = e.split(' ')
        return cmd, int(dist)
    return list(map(process, open(path).readlines()))


def q1(path):
    depth, dist = 0, 0
    for cmd, var in parse(path):
        if cmd == 'forward':
            dist += var
        elif cmd == 'up':
            depth -= var
        elif cmd == 'down':
            depth += var
    return depth * dist


def q2(path):
    depth, dist, aim = 0, 0, 0
    for cmd, var in parse(path):
        if cmd == 'forward':
            dist += var
            depth += var * aim
        elif cmd == 'up':
            aim -= var
        elif cmd == 'down':
            aim += var
    return depth * dist


if __name__ == '__main__':
    assert q1("test.txt") == 150
    print(q1("data.txt"))
    assert q2("test.txt") == 900
    print(q2("data.txt"))
