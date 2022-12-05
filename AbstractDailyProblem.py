import abc


class AbstractDailyProblem(abc.ABC):
    def __init__(self, q1_test_answer, q2_test_answer):
        self.__q1_test = q1_test_answer
        self.__q2_test = q2_test_answer

    def parse(self, input_path, entry_separator='\n'):
        return list(map(self.parse_entry, open(input_path).read().strip().split(entry_separator)))

    def parse_entry(self, entry):
        return entry

    @abc.abstractmethod
    def question_1(self, input_path) -> int:
        pass

    @abc.abstractmethod
    def question_2(self, input_path) -> int:
        pass

    def run(self, test_path="test.txt", input_path="input.txt") -> bool:
        try:
            assert self.question_1(test_path) == self.__q1_test
        except AssertionError:
            print(f"Question 1 fails: expected {self.__q1_test}, found {self.question_1(test_path)}")
            return False

        print(f"Answer #1: {self.question_1(input_path)}")

        try:
            assert self.question_2(test_path) == self.__q2_test
        except AssertionError:
            print(f"Question 2 fails: expected {self.__q2_test}, found {self.question_2(test_path)}")
            return False

        print(f"Answer #2: {self.question_2(input_path)}")
        return True
