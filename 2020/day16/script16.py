def read_input(path):
    valid_values = {}
    your_ticket, near_ticket = [], [[]]
    with open(path) as f:
        line = f.readline()
        while line.strip() != "":
            a1, a2 = line.strip().split(": ")
            a3, a4 = a2.split(" or ")
            valid_values[a1] = [list(map(int, a3.split('-'))), list(map(int, a4.split('-')))]
            line = f.readline()

        f.readline()  # jump to "your ticket"
        line = f.readline()  # jump over "your ticket"
        your_ticket = list(map(int, line.strip().split(',')))

        f.readline()  # jump to blank space
        f.readline()  # jump to nearby_tickets
        near_ticket = [list(map(int, line.strip().split(','))) for line in f.readlines()]

    return valid_values, your_ticket, near_ticket


def q1(path):
    valid_values, your_ticket, near_tickets = read_input(path)
    error_rate = 0
    for ticket in near_tickets:
        for value in ticket:
            if not any(any(_[0] <= value <= _[1] for _ in ranges) for ranges in valid_values.values()):
                error_rate += value
    return error_rate


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
    print(q1("input.txt"))
    print(q2("input.txt"))
