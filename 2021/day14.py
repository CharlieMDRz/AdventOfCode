from collections import Counter
from typing import Dict, Tuple


def load_input(file_path: str) -> Tuple[str, Dict[str, str]]:
    input_lines = open(file_path).read().split('\n')
    polymer = input_lines[0]

    mutation_rules = {}
    for mutation_rule in input_lines[2:]:
        pair, insert = mutation_rule.split(' -> ')
        mutation_rules[pair] = insert

    return polymer, mutation_rules


def mutate(polymer: str, mutation_rules: Dict[str, str]) -> str:
    mutation = polymer[0]
    for index in range(len(polymer) - 1):
        pair = polymer[index: index+2]
        mutation += mutation_rules[pair]
        mutation += pair[1]
    return mutation


def q1(file_path):
    polymer, rules = load_input(file_path)
    for _ in range(10):
        polymer = mutate(polymer, rules)

    occurrences = Counter(polymer)
    return max(occurrences.values()) - min(occurrences.values())


def q2(file_path):
    polymer, rules = load_input(file_path)
    polymer_pairs = init_pairs_from_polymer(polymer)
    for _ in range(40):
        polymer_pairs = mutate_pairs(polymer_pairs, rules)

    letter_count = {polymer[0]: .5, polymer[-1]: .5}
    for pair, count in polymer_pairs.items():
        for letter in pair:
            letter_count.setdefault(letter, 0)
            letter_count[letter] += count / 2
    return max(letter_count.values()) - min(letter_count.values())


def init_pairs_from_polymer(polymer: str):
    pair_count = {}
    for index in range(len(polymer) - 1):
        pair = polymer[index: (index+2)]
        pair_count.setdefault(pair, 0)
        pair_count[pair] += 1
    return pair_count


def mutate_pairs(pair_count: Dict[str, int], mutation_rules: Dict[str, str]):
    mutation = {}
    for pair, count in pair_count.items():
        insertion = mutation_rules[pair]
        for sub_pair in (pair[0] + insertion, insertion + pair[1]):
            mutation.setdefault(sub_pair, 0)
            mutation[sub_pair] += count

    return mutation


if __name__ == '__main__':
    test_path = 'resources/2021/14/test.txt'
    test_poly, test_rules = load_input(test_path)
    print(test_poly, test_rules)
    print(mutate(test_poly, test_rules))
    assert q1(test_path) == 1588
    assert q2(test_path) == 2188189693529

    print(f'q1 answer: {q1("resources/2021/14/data.txt")}')
    print(f'q2 answer: {q2("resources/2021/14/data.txt")}')
