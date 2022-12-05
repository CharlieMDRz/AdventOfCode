from numpy import array, ndarray


def parse(path) -> ndarray:
    def process(e):
        return [int(_) for _ in e.strip()]
    return array(list(map(process, open(path).readlines())))


def most_common(matrix):
    half_count = matrix.shape[0] / 2
    return (matrix.sum(0) >= half_count).astype(int)


def least_common(matrix):
    half_count = matrix.shape[0] / 2
    return (matrix.sum(0) < half_count).astype(int)


def bitlist_to_int(list) -> int:
    val = 0
    for b in list:
        val = (val << 1) | b
    return val


def q1(path):
    data = parse(path)
    gamma_bits, eps_bits = most_common(data), least_common(data)
    print(gamma_bits, eps_bits)
    gamma = bitlist_to_int(gamma_bits)
    eps = bitlist_to_int(eps_bits)
    return gamma * eps


def q2(path):
    data = parse(path)
    i = 0
    while data.shape[0] > 1:
        b = most_common(data)[i]
        data = data[(data[:, i] == b)]
        i += 1
    oxy = bitlist_to_int(data.flatten())
    data = parse(path)
    i = 0
    while data.shape[0] > 1:
        b = least_common(data)[i]
        data = data[(data[:, i] == b)]
        i += 1
    co2 = bitlist_to_int(data.flatten())
    return oxy * co2


if __name__ == '__main__':
    assert q1("test.txt") == 198
    print(q1("data.txt"))
    assert q2("test.txt") == 230
    print(q2("data.txt"))
