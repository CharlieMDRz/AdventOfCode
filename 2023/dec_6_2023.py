import math

import tqdm

from AbstractDailyProblem import AbstractDailyProblem


def hold_solutions(race_duration: int, record: int) -> int:
    """ doc """
    def distance(charge_time: int) -> int:
        """Compute distance ran when holding the button for charge_time seconds"""
        return max(0, charge_time * (race_duration - charge_time))

    return len([t for t in range(race_duration) if distance(t) > record])


class Advent2023day6(AbstractDailyProblem):
    """2023-12-06"""

    def __init__(self) -> None:
        super().__init__(288, 71503)

    def parse(self, input_path: str, entry_separator='\n') -> list[tuple[int, int]]:
        lines = super().parse(input_path, entry_separator)
        assert len(lines) == 2
        return list(zip(lines[0], lines[1]))

    def parse_entry(self, entry: str):
        return [int(_) for _ in entry.split(' ')[1:] if _]

    def question_1(self, input_path) -> int:
        res = 1
        for race_duration, record in self.parse(input_path):
            res *= hold_solutions(race_duration, record)
        return res

    def question_2(self, input_path) -> int:
        races = self.parse(input_path)
        race_duration = int(''.join(map(str, [_[0] for _ in races])))
        record = int(''.join(map(str, [_[1] for _ in races])))
        # Solve distance(hold_duration) > race_record as a 2nd degree polynomial equation
        # -X**2 + race_duration * X - record > 0
        a, b, c = -1, race_duration, -record
        delta = b**2 - 4*a*c
        first_root: float = (-b - math.sqrt(delta)) / (2*a)
        second_root: float = (-b + math.sqrt(delta)) / (2*a)
        # return int(math.floor(first_root) - math.ceil(second_root) + 1)
        return hold_solutions(race_duration, record)


if __name__ == '__main__':
    Advent2023day6().run('../resources/2023/6/test.txt', '../resources/2023/6/input.txt')
