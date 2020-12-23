from itertools import product
from typing import Set

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


def apply_mask(mask, val):
    bin_val = '{0:b}'.format(val)
    if len(bin_val) < len(mask):
        bin_val = '0' * (len(mask) - len(bin_val)) + bin_val
    for pos, char in enumerate(mask):
        if char != 'X':
            bin_val = bin_val[:pos] + char + bin_val[(pos+1):]
    return int(bin_val, 2)


def q1():
    import re
    print("Q1")
    registers = {}
    mask = 0
    for line in open('input.txt').readlines():
        if line.startswith('mask'):
            mask = line.strip().split('= ')[1].lstrip('X')
        elif line.startswith('mem'):
            m = re.search('mem\[(\d+)\] = (\d+)', line)
            reg, val = int(m.group(1)), int(m.group(2))
            registers[reg] = apply_mask(mask, val)
    print(sum(registers.values()))


def get_address(mask: str, val: str or int, i: int = 0) -> Set[int]:
    if i == 0:
        val = '{0:b}'.format(val)
        if len(val) < len(mask):
            val = '0' * (len(mask) - len(val)) + val
    elif i == len(mask):
        #print("end", val, int(val, 2), i)
        return {int(val, 2)}

    #print(mask[i], val, i)
    if mask[i] == '0':
        return get_address(mask, val, i+1)
    elif mask[i] == '1':
        val = val[:i] + '1' + val[(i+1):]
        return get_address(mask, val, i+1)
    elif mask[i] == 'X':
        val1 = val[:i] + '0' + val[(i+1):]
        val2 = val[:i] + '1' + val[(i+1):]
        return get_address(mask, val1, i+1).union(get_address(mask, val2, i+1))


def q2():
    import re
    print("Q2")
    registers = {}
    mask = 0
    for line in open('input.txt').readlines():
        from time import sleep
        sleep(0.001)
        if line.startswith('mask'):
            mask = line.strip().split('= ')[1].lstrip('0')
        elif line.startswith('mem'):
            m = re.search('mem\[(\d+)\] = (\d+)', line)
            reg, val = int(m.group(1)), int(m.group(2))
            for reg_dec in get_address(mask, reg):
                registers[reg_dec] = val
    print(sum(registers.values()))


if __name__ == '__main__':
    mask = '1XXXX0X'
    val = 11
    print(apply_mask(mask, val))
    print(q1())

    print("Test Q2")
    mask = '000000000000000000000000000000X1001X'
    val = 42
    print(get_address(mask, val))
    print(q2())
