from typing import List, Tuple


def parse(path):
    def process(e):
        return list(e.strip())
    return list(map(process, open(path).readlines()))


closure = {'{': '}', '[': ']', '(': ')', '<': '>'}


def solve(line: List[str]) -> Tuple[List[str], str]:
    lifo = []
    for char in line:
        if char in closure.values():
            last_char = lifo.pop()
            if closure[last_char] != char:
                return lifo + [last_char], char
        else:
            lifo.append(char)
    return lifo, ''


def q1(path):
    data = parse(path)
    score = {')': 3, ']': 57, '}': 1197, '>': 25137}

    def line_score(solution):
        last_char = solution[-1]
        if not last_char:
            return 0
        else:
            return score[last_char]

    return sum(map(line_score, map(solve, data)))


def q2(path):
    score = {')': 1, ']': 2, '}': 3, '>': 4}
    data = parse(path)

    def line_score(solved_line):
        res = 0
        for char in reversed(solved_line):
            res = res * 5 + score[closure[char]]
        return res

    scores = sorted(line_score(line) for (line, char) in map(solve, data) if not char)
    return scores[len(scores) // 2]


if __name__ == '__main__':
    assert q1("test.txt") == 26397
    print(q1("data.txt"))
    assert q2("test.txt") == 288957
    print(q2("data.txt"))
