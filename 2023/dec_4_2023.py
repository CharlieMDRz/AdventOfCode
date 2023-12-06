from AbstractDailyProblem import AbstractDailyProblem


def matches(winning_numbers: list[int], card_numbers: list[int]) -> int:
    return len([_ for _ in card_numbers if _ in winning_numbers])

def card_score(winning_numbers: list[int], card_numbers: list[int]) -> int:
    wins = matches(winning_numbers, card_numbers)
    if wins == 0:
        return 0
    return 1 << (wins - 1)


class Advent2023day4(AbstractDailyProblem):
    """2023-12-04"""

    def __init__(self) -> None:
        super().__init__(13, 30)

    def parse_entry(self, entry: str):
        data = entry.strip().split(': ')[1]
        return map(lambda values_str: [int(_) for _ in values_str.split(' ') if _], data.split('|'))

    def question_1(self, input_path: str) -> int:
        return sum(card_score(*_) for _ in self.parse(input_path))

    def question_2(self, input_path: str) -> int:
        cards = list(self.parse(input_path))
        # start with one card of each value, enumerated from zero cause f it
        deck = {i: 1 for i in range(len(cards))}
        for card_id, card in enumerate(cards):
            for card_delta in range(matches(*card)):
                deck[card_id + card_delta + 1] += deck[card_id]
        return sum(deck.values())


if __name__ == '__main__':
    Advent2023day4().run('../resources/2023/4/test.txt', '../resources/2023/4/input.txt')
