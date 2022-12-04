def process_line(e: str):
    if e == '':
        return ''
    sep = ',' if ',' in e else ' '
    return [int(_) for _ in e.strip().split(sep) if _]


def parse(path: str):
    from numpy import array
    path = str(__file__) + '/../' + path
    lines = list(map(process_line, open(path).readlines()))
    pool, board_lines = lines[0], lines[1:]
    n_boards = len(board_lines) // 6
    boards = [array(board_lines[(6*i + 1):(6*i + 6)]) for i in range(n_boards)]
    return boards, pool


def wins(board, pool):
    from numpy import vectorize
    masked_board = vectorize(lambda _: _ in pool)(board)
    return any(masked_board.all(0)) or any(masked_board.all(1))


def score(board, pool):
    from numpy import vectorize
    unmarked_board = vectorize(lambda _: 0 if _ in pool else _)(board)
    return unmarked_board.sum() * pool[-1]


def question1(path: str) -> int:
    boards, pool = parse(path)
    seen_pool = [pool.pop(0)]
    while not any(wins(b, seen_pool) for b in boards):
        seen_pool.append(pool.pop(0))
    winning_board = next(b for b in boards if wins(b, seen_pool))
    return score(winning_board, seen_pool)


def question2(path: str) -> int:
    boards, pool = parse(path)
    seen_pool = [pool.pop(0)]
    while not all(wins(b, seen_pool) for b in boards):
        boards = list(filter(lambda b: not wins(b, seen_pool), boards))
        seen_pool.append(pool.pop(0))
    winning_board = next(b for b in boards if wins(b, seen_pool))
    return score(winning_board, seen_pool)


if __name__ == "__main__":
    assert question1('test.txt') == 4512
    print("Answer #1: ", question1('input.txt'))
    assert question2('test.txt') == 1924
    print("Answer #2: ", question2('input.txt'))
