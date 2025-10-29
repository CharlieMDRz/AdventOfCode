import itertools

from AbstractDailyProblem import AbstractDailyProblem


class IntcodeComputer:
    def __init__(self, program: list[int]) -> None:
        self.__memory = program.copy()
        self.__operations = {
            1: (self.add, 3),
            2: (self.mult, 3),
            99: (self.halt, 0),
        }
        self.__pointer = 0
        self.__is_halted = False

    def run(self) -> int:
        try:
            while not self.__is_halted:
                self.operate()
            return self[0]
        except (KeyError, IndexError):
            pass

    def operate(self) -> None:
        opcode = self.__memory[self.__pointer]
        operation, nargs = self.__operations[opcode]
        parameters = [self[self.__pointer + i + 1] for i in range(nargs)]
        operation(*parameters)
        self.__pointer += nargs + 1

    def add(self, reg1: int, reg2: int, reg3: int) -> None:
        self.__memory[reg3] = self[reg1] + self[reg2]

    def mult(self, reg1: int, reg2: int, reg3: int) -> None:
        self.__memory[reg3] = self[reg1] * self[reg2]

    def halt(self) -> None:
        self.__is_halted = True

    def __getitem__(self, item: int) -> int:
        return self.__memory[item]


class Advent2019day2(AbstractDailyProblem):

    def question_2(self, input_path: str) -> int:
        output = 19690720
        program = self.parse(input_path)[0]
        for noun, verb in itertools.product(range(100), range(100)):
            program[1:3] = noun, verb
            res = IntcodeComputer(program).run()
            if res == output:
                break

        return 100 * noun + verb

    def question_1(self, input_path: str) -> int:
        program = self.parse(input_path)[0]
        if "input" in input_path:
            program[1:3] = 12, 2
        return IntcodeComputer(program).run()

    def parse_entry(self, entry: str) -> object:
        return list(map(int, entry.split(',')))

    def __init__(self) -> None:
        super().__init__(3500, 9999)


if __name__ == '__main__':
    Advent2019day2().run('../resources/2019/2/test.txt', '../resources/2019/2/input.txt')
