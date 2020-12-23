import re


class Graph:
    def __init__(self):
        self.vertices = set()
        self.edges = dict()

    def __add__(self, other):
        v1, v2, c = other
        if v1 not in self.edges:
            self.edges[v1] = dict()
        if v2 not in self.edges:
            self.edges[v2] = dict()
        self.edges[v1][v2] = c


def read_input():
    data = Graph()
    for line in open('input.txt').readlines():
        line = line.strip()
        expressions = re.findall('([0-9]+ )?([a-z ]+)bag', line)
        bag1 = expressions[0]
        col1 = bag1[1].strip()
        for bag2 in expressions[1:]:
            count, col2 = int(bag2[0]), bag2[1].strip()
            data.__add__((col2, col1, count))
    return data


def read_input2():
    data = Graph()
    for line in open('input.txt').readlines():
        print(line)
        line = line.strip()
        if line.__contains__('no other'):
            continue
        else:
            expressions = re.findall('([0-9]+ )?([a-z ]+)bags?', line)
            bag1 = expressions[0]
            col1 = bag1[1].strip()
            for bag2 in expressions[1:]:
                count, col2 = int(bag2[0]), bag2[1].strip()
                data.__add__((col1, col2, count))
            print(data.edges[col1])
    return data


def q1():
    data = read_input()
    color = 'shiny gold'
    valid_colors = set()

    def explore(graph, col1):
        for col2 in graph.edges[col1]:
            if col2 not in valid_colors:
                valid_colors.add(col2)
                explore(graph, col2)

    explore(data, color)
    print(len(valid_colors))


def q2():
    data = read_input2()
    color = 'shiny gold'

    def explore(graph, col1):
        print(col1, graph.edges[col1])
        if len(graph.edges[col1]) == 0:
            print('feuille')
            return 1
        else:
            return 1 + sum(graph.edges[col1][col2] * explore(graph, col2) for col2 in graph.edges[col1])

    print(explore(data, color) - 1)


if __name__ == '__main__':
    q1()
    q2()
