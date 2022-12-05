from typing import List, Set


def parse(path):
    def process(e):
        digits, code = map(lambda _: [''.join(sorted(c)) for c in _.strip().split(' ')], e.split("|"))
        return digits, code
    return list(map(process, open(path).readlines()))


def q1(path):
    data = parse(path)
    unique = {2, 3, 4, 7}
    return sum(len([_ for _ in item[1] if len(_) in unique]) for item in data)


def decode(digits: List[Set[str]]):
    decoder = {}
    encoder = {}
    for length, value in {(7, 8), (2, 1), (3, 7), (4, 4)}:
        code = next(_ for _ in digits if len(_) == length)
        decoder[code] = value
        encoder[value] = code
        digits.remove(code)

    code9 = next(_ for _ in digits if set(encoder[4]).issubset(set(_)))
    decoder[code9] = 9
    encoder[9] = code9
    digits.remove(code9)

    code0 = next(_ for _ in digits if set(encoder[1]).issubset(set(_)) and len(_) == 6)
    decoder[code0] = 0
    encoder[0] = code0
    digits.remove(code0)

    code6 = next(_ for _ in digits if len(_) == 6)
    decoder[code6] = 6
    encoder[6] = code6
    digits.remove(code6)

    code3 = next(_ for _ in digits if set(encoder[7]).issubset(set(_)))
    decoder[code3] = 3
    encoder[3] = code3
    digits.remove(code3)

    code5 = next(_ for _ in digits if set(_).issubset(set(encoder[6])))
    decoder[code5] = 5
    encoder[5] = code5
    digits.remove(code5)

    code2 = digits.pop()
    decoder[code2] = 2
    encoder[2] = code2

    return decoder


def value(decoder, code):
    return int(''.join(str(decoder[_]) for _ in code))


def q2(path):
    # return sum(value(dec, code) for dec, code in map(lambda _: (decode(_[0]), _[1]), parse(path)))
    data = parse(path)
    res = 0
    for message, code in data:
        decoder = decode(message)
        print(code, value(decoder, code))
        res += value(decoder, code)

    return res


if __name__ == '__main__':
    assert q1("test.txt") == 26
    print(q1("data.txt"))
    sample = parse('sample.txt')[0]
    print(sample)
    dec = decode(sample[0])
    print(dec, value(dec, sample[1]))
    assert q2("test.txt") == 61229
    print(q2("data.txt"))
