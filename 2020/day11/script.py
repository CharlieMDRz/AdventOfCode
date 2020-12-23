from itertools import product
from numpy import array, full


def read_data(path): return array(list(map(lambda v: list(v.strip()), open(path).readlines())))


def get_surrounding(seats, i, j):
    H, W = seats.shape
    subarray = seats[max(0, i-1):min(i+2, H), max(0, j-1):(min(j+2, W))]
    # flatten
    return subarray.flatten()


def iterate(seat_map):
    H, W = seat_map.shape
    new_seats = full((H, W), '.')
    for i, j in product(range(H), range(W)):
        surr = get_surrounding(seat_map, i, j)
        if seat_map[i][j] == 'L':
            new_seats[i][j] = '#' if all(v != '#' for v in surr) else 'L'
        elif seat_map[i][j] == '#':
            new_seats[i][j] = 'L' if (sum(surr == '#') > 4) else '#'

    return new_seats


def iterate2(seat_map):
    H, W = seat_map.shape
    new_seats = full((H, W), '.')
    for i, j in product(range(H), range(W)):
        surr = get_surrounding_taken_seat(seat_map, i, j)
        if seat_map[i][j] == 'L':
            new_seats[i][j] = '#' if surr == 0 else 'L'
        elif seat_map[i][j] == '#':
            new_seats[i][j] = 'L' if surr > 4 else '#'

    return new_seats


def get_surrounding_taken_seat(seats, i, j):
    res = 0
    H, W = seats.shape
    for di, dj in product([-1, 0, 1], [-1, 0, 1]):
        if di == 0 and dj == 0:
            continue
        i0 = i + di
        j0 = j + dj
        while 0 <= i0 < H and 0 <= j0 < W:
            if seats[i0, j0] == '#':
                res += 1
                break
            elif seats[i0, j0] == 'L':
                break
            i0 += di
            j0 += dj

    return res


def q1():
    seats = read_data('input.txt')
    H, W = seats.shape
    while True:
        update = iterate(seats)
        if all(update[i, j] == seats[i, j] for i, j in product(range(H), range(W))):
            return sum(sum(update == '#'))
        seats = update


def q2():
    seats = read_data('input.txt')
    H, W = seats.shape
    while True:
        update = iterate2(seats)
        if all(update[i, j] == seats[i, j] for i, j in product(range(H), range(W))):
            return sum(sum(update == '#'))
        seats = update


if __name__ == '__main__':
    test = read_data('test1.txt')
    print(test)
    print(get_surrounding(test, 0, 0))
    print(get_surrounding(test, 1, 0))
    print(get_surrounding(test, 1, 1))
    print(get_surrounding(test, 1, 1)=='L')
    print(get_surrounding(test, 0, 1))
    print(q2())