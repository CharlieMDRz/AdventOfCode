from typing import List, Dict


def process_line(e: str):
    return e.strip().split('-')


def parse(path: str):
    path = str(__file__) + '/../' + path
    graph = {}
    for a, b in map(process_line, open(path).readlines()):
        if a not in graph:
            graph[a] = []
        graph[a].append(b)

        if b not in graph: graph[b] = []
        graph[b].append(a)

    for n in graph:
        graph[n] = sorted(graph[n])

    return graph


def question1(path: str, do_print=False) -> int:
    graph: Dict[str, List[str]] = parse(path)

    def paths_to_end_that_start_with(part_path: List[str]) -> List[List[str]]:
        cur_node = part_path[-1]
        res: List[List[str]] = []
        if cur_node == 'end':
            res.append(part_path)
        else:
            for next_node in filter(lambda node: (node.upper() == node) or node not in part_path, graph[cur_node]):
                res.extend(paths_to_end_that_start_with(part_path + [next_node]))
        return res

    res = paths_to_end_that_start_with(['start'])
    if do_print:
        print('\n'.join(','.join(path) for path in res))
    return len(res)


def question2(path: str, do_print=False) -> int:
    graph: Dict[str, List[str]] = parse(path)

    def paths_to_end_that_start_with(part_path: List[str], can_reexplore) -> List[List[str]]:
        cur_node = part_path[-1]
        res: List[List[str]] = []
        if cur_node == 'end':
            res.append(part_path)
        else:
            for next_node in filter(lambda node: (node.upper() == node) or (node not in part_path) or (node != 'start' and can_reexplore), graph[cur_node]):
                b = can_reexplore and (next_node.upper() == next_node or next_node not in part_path)
                res.extend(paths_to_end_that_start_with(part_path + [next_node], b))
        return res

    res = paths_to_end_that_start_with(['start'], True)
    if do_print:
        print('\n'.join(','.join(path) for path in res))
    return len(res)


if __name__ == "__main__":
    assert question1('test.txt', True) == 10
    print("Answer #1: ", question1('input.txt'))
    assert question2('test.txt', True) == 36
    print("Answer #2: ", question2('input.txt'))
