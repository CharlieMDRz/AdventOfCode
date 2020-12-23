from numpy import array, zeros
from itertools import product

def init_array(path, cycles):
    cycles += 1
    def line_to_list(line):
        return [int(_ == '#') for _ in line.strip()]
    input_array = array(list(map(line_to_list, open(path).readlines())))
    print(input_array)
    full_array = zeros((input_array.shape[0] + 2*cycles,
                        input_array.shape[1] + 2*cycles,
                        2*cycles, 2*cycles))
    full_array[cycles:-cycles, cycles:-cycles, cycles, cycles] = input_array
    return full_array


def q1(path, c):
    space = init_array(path, c)
    X, Y, Z, W = space.shape
    i = 2
    print(space.shape)
    print(range(c-i, X-c+i))
    print(range(c-i, c+i+1))
    for i in range(1, c+1):
        next_space = zeros(space.shape)
        pass
        for x, y, z, w in product(range(c-i, X-c+i), range(c-i, Y-c+i), range(c-i, c+2+i), range(c-i, c+2+i)):
            surr = space[(x-1):(x+2), (y-1):(y+2), (z-1):(z+2), (w-1):(w+2)].sum() - space[x, y, z, w]
            if space[x, y, z, w]:
                next_space[x, y, z, w] = int(surr in [2, 3])
            else:
                next_space[x, y, z, w] = int(surr == 3)
        space = next_space
        # print("run {}".format(i))
        # for z in range(next_space.shape[2]):
        #     if next_space[:, :, z].sum():
        #         print("z={}".format(z-c))
        #         print(next_space[(c-i+1):(X-c+i-1), (c-i+1):(X-c+i-1), z])
    return space.sum()


def q2(path):
    valid_values, your_ticket, near_tickets = read_input(path)
    near_valid = []
    for ticket in near_tickets:
        if all(any(any(_[0] <= value <= _[1] for _ in ranges) for ranges in valid_values.values()) for value in ticket):
            near_valid.append(ticket)

    field_to_index = {}
    while len(valid_values):
        for index in range(len(near_valid[0])):
            values = [ticket[index] for ticket in near_valid]
            index_match = {_ for _ in filter(lambda field: all(any(_[0] <= value <= _[1] for _ in valid_values[field]) for value in values), valid_values)}
            if len(index_match) == 1:
                field = index_match.pop()
                field_to_index[field] = index
                del valid_values[field]
    print(field_to_index)
    print(your_ticket)
    res = 1
    for field in filter(lambda k: k.startswith("departure"), field_to_index):
        print(field, field_to_index[field], your_ticket[field_to_index[field]])
        res *= your_ticket[field_to_index[field]]
    return res


if __name__ == '__main__':
    #print(read_input('test.txt'))
    # print(init_array("test.txt", 2))
    print(q1("input.txt", 6))
