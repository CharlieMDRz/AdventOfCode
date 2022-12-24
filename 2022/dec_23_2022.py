from typing import Tuple, Set

from AbstractDailyProblem import AbstractDailyProblem

ElfPosition = Tuple[int, int]


def next_move(round_id: int, elf_pos: ElfPosition, elves: Set[ElfPosition]) -> ElfPosition:
    x, z = elf_pos
    n_pos = (x - 1, z)
    s_pos = (x + 1, z)
    e_pos = (x, z + 1)
    w_pos = (x, z - 1)
    ne_pos = (x - 1, z + 1)
    se_pos = (x + 1, z + 1)
    nw_pos = (x - 1, z - 1)
    sw_pos = (x + 1, z - 1)

    # decide not to move if no neighbour
    if not any(pos in elves for pos in [n_pos, s_pos, e_pos, w_pos, ne_pos, nw_pos, se_pos, sw_pos]):
        return elf_pos

    decision_order = [None if elves.intersection((n_pos, ne_pos, nw_pos)) else n_pos,
                      None if elves.intersection((s_pos, se_pos, sw_pos)) else s_pos,
                      None if elves.intersection((w_pos, nw_pos, sw_pos)) else w_pos,
                      None if elves.intersection((e_pos, ne_pos, se_pos)) else e_pos]

    for index in range(4):
        decision_index = (index + round_id) % 4
        if decision_order[decision_index] is not None:
            return decision_order[decision_index]
    return elf_pos


def do_round(round_id: int, elves_positions: Set[ElfPosition]) -> Tuple[Set[ElfPosition], bool]:
    move_decisions = {}
    moved = False

    for elf_pos in elves_positions:
        move_decisions.setdefault(next_move(round_id, elf_pos, elves_positions), []).append(elf_pos)

    new_positions = set()
    for new_pos, prev_positions in move_decisions.items():
        if len(prev_positions) == 1:
            new_positions.add(new_pos)
            if new_pos != prev_positions[0]:
                moved = True
        else:
            new_positions.update(prev_positions)
    return new_positions, moved


def display(elves_pos: Set[ElfPosition]):
    min_x = min(pos[0] for pos in elves_pos)
    max_x = max(pos[0] for pos in elves_pos)
    min_z = min(pos[1] for pos in elves_pos)
    max_z = max(pos[1] for pos in elves_pos)

    grid = [['.' for _ in range(min_z, max_z + 1)] for _ in range(min_x, max_x + 1)]
    for x, z in elves_pos:
        grid[x - min_x][z - min_z] = '#'

    print('\n'.join(map(''.join, grid)))
    print()


class Advent2022day23(AbstractDailyProblem):

    def parse_entry(self, entry):
        return [z for z, char in enumerate(entry.strip()) if char == '#']

    def parse(self, input_path, entry_separator='\n') -> Set[ElfPosition]:
        initial_elf_pos = set()
        raw_pos = super().parse(input_path, entry_separator)
        for x, z_list in enumerate(raw_pos):
            for z in z_list:
                initial_elf_pos.add((x, z))

        return initial_elf_pos

    def question_1(self, input_path) -> int:
        elves_pos = self.parse(input_path)
        for _ in range(10):
            elves_pos, _ = do_round(_, elves_pos)

        min_x = min(pos[0] for pos in elves_pos)
        max_x = max(pos[0] for pos in elves_pos)
        min_z = min(pos[1] for pos in elves_pos)
        max_z = max(pos[1] for pos in elves_pos)

        return (max_x - min_x + 1) * (max_z - min_z + 1) - len(elves_pos)

    def question_2(self, input_path) -> int:
        elves_pos = self.parse(input_path)
        round_id = 0
        while True:
            elves_pos, moved = do_round(round_id, elves_pos)
            if moved:
                round_id += 1
            else:
                return round_id + 1

    def __init__(self):
        super().__init__(110, 20)


if __name__ == '__main__':
    Advent2022day23().run('../resources/2022/23/test.txt', '../resources/2022/23/input.txt')
