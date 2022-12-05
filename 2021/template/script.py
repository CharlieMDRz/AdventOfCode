def parse(path):
    def process(e):
        return e
    return list(map(process, open(path).readlines()))


def q1(path):
    return 0


def q2(path):
    return 0


if __name__ == '__main__':
    assert q1("test.txt") == 0
    print(q1("data.txt"))
    assert q2("test.txt") == 0
    print(q2("data.txt"))
