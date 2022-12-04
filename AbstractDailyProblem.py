import abc


class AbstractDailyProblem(abc.ABC):
    def __init__(self, q1_test_answer, q2_test_answer):
        self.__q1_test = q1_test_answer
        self.__q2_test = q2_test_answer

    @abc.abstractmethod
    def parse(self, input_path):
        pass

    @abc.abstractmethod
    def question_1(self, input_path) -> int:
        pass

    @abc.abstractmethod
    def question_2(self, input_path) -> int:
        pass

    def run(self) -> bool:
        try:
            assert self.question_1("test.txt") == self.__q1_test
        except AssertionError:
            print(f"Question 1 fails: expected {self.__q1_test}, found {self.question_1('test.txt')}")
            return False

        print(f"Answer #1: {self.question_1('input.txt')}")

        try:
            assert self.question_2("test.txt") == self.__q2_test
        except AssertionError:
            print(f"Question 2 fails: expected {self.__q2_test}, found {self.question_2('test.txt')}")
            return False

        print(f"Answer #2: {self.question_2('input.txt')}")
        return True
