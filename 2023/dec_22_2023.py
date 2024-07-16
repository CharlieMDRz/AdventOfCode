import attrs
import networkx as nx

from AbstractDailyProblem import AbstractDailyProblem


@attrs.define()
class Brick:
    id: int
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int

    def drop_down(self):
        self.z1 -= 1
        self.z2 -= 1

    @property
    def coords(self):
        return [
            (x, y, z)
            for x in range(self.x1, self.x2+1)
            for y in range(self.y1, self.y2+1)
            for z in range(self.z1, self.z2+1)
        ]


def can_drop(brick: Brick, bricks):
    if brick.z1 == 1:
        return False
    else:
        return all(bricks.get((x, y, z-1), brick.id) == brick.id for x, y, z in brick.coords)


def can_disintegrate(brick_id: int, brick_graph: nx.DiGraph) -> bool:
    try:
        return all(brick_graph.in_degree[supported_brick] > 1 for supported_brick in brick_graph.successors(brick_id))
    except Exception:
        # Unlinked bricks
        return True


def collapsed_by(brick_id: int, brick_graph: nx.DiGraph) -> int:
    collapsed = set()
    to_collapse = [brick_id]
    if brick_id not in brick_graph:
        return 0
    while to_collapse:
        brick_id = to_collapse.pop(0)
        collapsed.add(brick_id)
        to_collapse.extend(
            [_ for _ in brick_graph.successors(brick_id) if all(pred in collapsed for pred in brick_graph.predecessors(_))]
        )

    return len(collapsed) - 1


class Advent2023day22(AbstractDailyProblem):

    def question_2(self, input_path) -> int:
        brick_list = [Brick(i, *c) for i, c in enumerate(self.parse(input_path))]
        brick_mesh = {
            coord: brick.id
            for brick in brick_list
            for coord in brick.coords
        }
        do_update = True
        while do_update:
            do_update = False
            for brick in sorted(brick_list, key=lambda b: b.z1):
                if can_drop(brick, brick_mesh):
                    do_update = True
                    for pos in brick.coords:
                        brick_mesh.pop(pos)
                    brick.drop_down()
                    brick_mesh.update({pos: brick.id for pos in brick.coords})

        support_graph = nx.DiGraph()
        for brick in brick_list:
            for supported_brick in {
                brick_mesh.get((x, y, z + 1), brick.id) for x, y, z in brick.coords
            }.difference({brick.id}):
                support_graph.add_edge(brick.id, supported_brick)

        return sum(collapsed_by(brick.id, support_graph) for brick in brick_list)


    def question_1(self, input_path) -> int:
        brick_list = [Brick(i, *c) for i, c in enumerate(self.parse(input_path))]
        brick_mesh = {
            coord: brick.id
            for brick in brick_list
            for coord in brick.coords
        }
        do_update = True
        while do_update:
            do_update = False
            for brick in sorted(brick_list, key=lambda b: b.z1):
                if can_drop(brick, brick_mesh):
                    do_update = True
                    for pos in brick.coords:
                        brick_mesh.pop(pos)
                    brick.drop_down()
                    brick_mesh.update({pos: brick.id for pos in brick.coords})

        support_graph = nx.DiGraph()
        for brick in brick_list:
            for supported_brick in {
                brick_mesh.get((x, y, z + 1), brick.id) for x, y, z in brick.coords
            }.difference({brick.id}):
                support_graph.add_edge(brick.id, supported_brick)

        return len([b for b in brick_list if can_disintegrate(b.id, support_graph)])


    def __init__(self):
        super().__init__(5, 7)

    def parse_entry(self, entry: str):
        return [int(coord) for position in entry.strip().split('~') for coord in position.split(',') ]


if __name__ == '__main__':
    Advent2023day22().run('../resources/2023/22/test.txt', '../resources/2023/22/input.txt')
