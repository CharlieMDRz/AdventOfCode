from typing import List

from AbstractDailyProblem import AbstractDailyProblem


class Advent2022day1(AbstractDailyProblem):

    def __init__(self):
        super().__init__(24000, 45000)

    def parse(self, input_path) -> List[List[int]]:
        data = open(input_path).read().strip()
        elves_data = data.split("\n\n")
        return [list(map(int, elf_data.split("\n"))) for elf_data in elves_data]

    def question_1(self, input_path) -> int:
        calories_per_elf = self.parse(input_path)
        return max(map(sum, calories_per_elf))

    def question_2(self, input_path) -> int:
        calories_per_elf = self.parse(input_path)
        calories_per_elf.sort(key=sum, reverse=True)
        return sum(map(sum, calories_per_elf[:3]))


if __name__ == '__main__':
    Advent2022day1().run()
