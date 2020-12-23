from itertools import product

def find_anomaly(l, preamble):
    end_index = preamble

    def next_is_valid():
        target_sum = l[end_index]
        window = l[(end_index - preamble):end_index]
        return any(u+v == target_sum for u, v in product(window, window))

    while next_is_valid():
        end_index += 1
    return l[end_index]

def find_range_sum(l, target):
    start_pos = 0
    while start_pos < len(l):
        end_pos = start_pos + 2
        while end_pos < len(l):
            part_l = l[start_pos:end_pos]
            part_sum = sum(part_l)
            if part_sum == target:
                return min(part_l) + max(part_l)
            elif part_sum > target:
                break
            else:
                end_pos += 1
        start_pos += 1
    return 0

if __name__ == "__main__":
    l = list(map(int, open('input.txt').readlines()))
    print(find_anomaly(l, 25))
    print(find_range_sum(l, 556543474))