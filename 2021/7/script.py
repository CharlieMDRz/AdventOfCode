def parse(path):
    return [int(_) for _ in open(path).readline().strip().split(',')]


def q1(path):
    from numpy import array

    pos_list = array(sorted(parse(path)))

    def cost(val):
        return sum(abs(pos_list - val))

    n = len(pos_list)
    if n % 2:
        sol = pos_list[(n+1) // 2]
    else:
        sol_id = (n // 2) if cost(pos_list[n // 2]) < cost(pos_list[n // 2 + 1]) else (n // 2 + 1)
        sol = pos_list[sol_id]
    return cost(sol)


def q2(path):
    from numpy import array

    pos_list = array(parse(path))

    def cost(val):
        err = abs(pos_list - val)
        # return (err.dot(err) + sum(err)) // 2
        cost_array = err * (err + 1) // 2
        return sum(cost_array)

    cost_dict = {}
    u, v = min(pos_list), max(pos_list)
    cost_dict[u] = cost(u)
    cost_dict[v] = cost(v)

    while abs(u - v) > 1:
        m = (u + v) // 2
        cost_dict[m] = cost(m)
        if cost_dict[v] < cost_dict[u]:
            u = m
        else:
            v = m

    return min(cost_dict[u], cost_dict[v])


if __name__ == '__main__':
    assert q1("test.txt") == 37
    print(q1("data.txt"))
    assert q2("test.txt") == 168
    from time import time_ns
    t0 = time_ns()
    print(q2("data.txt"))
    from timeit import timeit
    print(timeit('q2("data.txt")', globals=globals(), number=1000)/1000)
