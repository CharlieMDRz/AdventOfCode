ACC = 'acc'
NOP = 'nop'
JMP = 'jmp'


def run(lines):
    seen_lines = []
    accumulator = 0
    line_index = 0
    while line_index not in seen_lines and line_index < len(lines):
        line = lines[line_index].strip()
        seen_lines.append(line_index)
        if line[:3] == ACC:
            accumulator += int(line[4:])
            line_index += 1
        elif line[:3] == NOP:
            line_index += 1
        elif line[:3] == JMP:
            line_index += int(line[4:])
    return accumulator, seen_lines


def q1():
    lines = list(open('input.txt').readlines())
    res, _ = run(lines)
    return res


def q2():
    lines = list(open('input.txt').readlines())
    _, def_exec = run(lines)
    for index in filter(lambda i: lines[i][:3] in [NOP, JMP], def_exec):
        src, mod = (NOP, JMP) if (lines[index][:3] == NOP) else (JMP, NOP)
        lines[index] = mod + lines[index][3:]
        res, mod_exec = run(lines)
        if mod_exec[-1] == len(lines) - 1:
            return res
        else:
            lines[index] = src + lines[index][3:]


if __name__ == '__main__':
    print(q1())
    print(q2())
