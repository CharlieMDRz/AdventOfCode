def read_data(path): return [0] + sorted(map(int, open(path).readlines())) + [max(map(int, open(path).readlines()))+3]

def q1():
    data = read_data('input.txt')
    print(data)
    assert all(v - u <= 3 for u, v in zip(data[:-1], data[1:]))
    d1 = sum(int((v - u) == 1) for u, v in zip(data[:-1], data[1:]))
    d3 = sum(int((v - u) == 3) for u, v in zip(data[:-1], data[1:]))
    print(d1, d3, d1 * d3)

def q2():
    data = read_data('input.txt')
    elt_to_bin = {data[i]: 1<<i for i in range(len(data))}
    stor_res = {}
    print(data)
    def valid_arrangements(sorted_data, part_seq):
        array_id = sum(elt_to_bin[elt] for elt in sorted_data)
        if array_id in stor_res: return stor_res[array_id]
        if len(sorted_data) == 1:
            # print(part_seq + sorted_data)
            stor_res[array_id] = 1
            return 1
        res = 0
        head = sorted_data[0]
        i = 1
        while i < len(sorted_data) and sorted_data[i] <= head + 3:
            res += valid_arrangements(sorted_data[i:], part_seq + [head])
            i += 1
        stor_res[array_id] = res
        return res

    print(valid_arrangements(data, []))


if __name__ == '__main__':
    q1()
    q2()