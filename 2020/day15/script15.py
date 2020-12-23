from typing import Dict


class Game:
    def __init__(self, first_numbers):
        self.count = 1  # type: int
        self.last_turn_for_number = {}  # type: Dict[int, (int)]
        self.prev_turn = first_numbers[0]  # type: int
        for _ in first_numbers[1:]:
            self.last_turn_for_number[self.prev_turn] = self.count
            self.prev_turn = _
            self.count += 1

    def play(self):

        if self.prev_turn not in self.last_turn_for_number:
            next_turn = 0
        else:
            next_turn = self.count - self.last_turn_for_number[self.prev_turn]

        self.last_turn_for_number[self.prev_turn] = self.count
        self.prev_turn = next_turn
        self.count += 1


def q1():
    first_turns = [0, 3, 6]
    first_turns = [2, 0, 1, 9, 5, 19]
    game = Game(first_turns)
    print(game.last_turn_for_number, game.count, game.prev_turn)

    n_turns = 30000000
    for _ in range(n_turns - len(first_turns)):
        game.play()
        if game.count % (n_turns//100) == 0:
            print(game.count)
    print(game.count, game.prev_turn)


if __name__ == '__main__':
    q1()
