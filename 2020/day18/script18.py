from numpy import array, zeros
from itertools import product

ops = ['+', '*']


def parse(line):
    symbols = line.split()  # cuts around operators
    for spec in ['(', ')']:
        index = 0
        while index < len(symbols):
            if spec in symbols[index]:
                new_sym = list(map(lambda v: v if len(v) else spec, symbols[index].split(spec)))
                symbols = symbols[:index] + new_sym + symbols[(index+1):]
                index += len(new_sym)
            else:
                index += 1
    for _ in range(len(symbols)):
        try:
            symbols[_] = int(symbols[_])
        finally:
            continue
    return symbols


def op(int1: int, ope: str, int2: int) -> int:
    if ope == '+':
        return int1 + int2
    elif ope == '*':
        return int1 * int2
    else:
        raise ValueError("Unknown operator {}".format(ope))


def find_par_index(symbol_list):
    c = 0
    i_op = 0
    for i in range(len(symbol_list)):
        if symbol_list[i] == '(':
            if c == 0:
                i_op = i
            c += 1
        elif symbol_list[i] == ')':
            if c == 1:
                return i_op, i
            c -= 1
    return None


def evaluate(symbol_list):
    s = symbol_list
    if '(' in symbol_list:
        i, j = find_par_index(symbol_list)
        par_eval = evaluate(s[(i+1):j])
        return evaluate(s[:i] + par_eval + (s[(j+1):] if j+1 < len(s) else []))
    elif len(symbol_list) == 1:
        return symbol_list
    elif type(s[0]) is int and type(s[2]) is int:
        s = [op(s[0], s[1], s[2])] + (s[3:] if 3 < len(s) else [])
        return evaluate(s)
    else:
        raise ValueError("IDK", s[c:])


def evaluate2(symbol_list):
    s = symbol_list
    if '(' in symbol_list:
        i, j = find_par_index(symbol_list)
        par_eval = evaluate2(s[(i+1):j])
        return evaluate2(s[:i] + par_eval + (s[(j+1):] if j+1 < len(s) else []))
    elif '+' in symbol_list:
        i = symbol_list.index('+')
        s2 = s[:(i-1)] + evaluate(s[(i-1):(i+2)]) + (s[(i+2):] if i+2 < len(s) else [])
        return evaluate2(s2)
    elif len(symbol_list) == 1:
        return symbol_list
    elif type(s[0]) is int and type(s[2]) is int:
        s = [op(s[0], s[1], s[2])] + (s[3:] if 3 < len(s) else [])
        return evaluate2(s)
    else:
        raise ValueError("IDK", s)


def q1(path):
    return sum(evaluate(parse(_))[0] for _ in open(path).readlines())


def q2(path):
    return sum(evaluate2(parse(_))[0] for _ in open(path).readlines())


if __name__ == '__main__':
    for _ in open('test.txt').readlines():
        print(_)
        s = parse(_)
        print(s)
        print(evaluate(s)[0])
        print(evaluate2(s)[0])
    print(q1("input.txt"))
    print(q2("input.txt"))
