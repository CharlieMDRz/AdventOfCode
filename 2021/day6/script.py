from time import time, process_time


def process_line(e: str):
    return e


def parse(path: str):
    path = str(__file__) + '/../' + path
    return [int(_) for _ in open(path).readline().strip().split(',')]


def age(liste, cycle):
    for index, value in enumerate(liste):
        if value == 0:
            liste[index] = cycle
            liste.append(cycle + 3)
        else:
            liste[index] -= 1


def question1(path: str, ndays: int) -> int:
    liste = parse(path)
    # print('Initial state', liste)
    for day in range(ndays):
        age(liste, 6)
        # print(f'Day {day+1}', liste)
    return len(liste)


def question2(path: str, ndays: int, do_print: bool = False) -> int:
    liste = parse(path)
    age_dict = [0 for _ in range(9)]
    for _ in liste:
        age_dict[_] += 1
    for _ in range(ndays):
        age_dict.append(age_dict.pop(0))
        age_dict[6] += age_dict[-1]
    return sum(age_dict)


if __name__ == "__main__":
    assert question2('test.txt', 18) == 26
    print("Answer #1: ", question2('input.txt', 80))
    assert question2('test.txt', 18, True) == 26
    assert question2('test.txt', 256) == 26984457539
    t0 = time()
    ans = question2('input.txt', 256)
    t1 = time()
    print(f"Answer #2: {ans} solved in {t1 - t0}")
    from timeit import timeit
    nruns = 1000
    print(timeit("question2('input.txt', 256)", "from script import question2", number=nruns)/nruns*10**6, "µs") # print exec time in mus
