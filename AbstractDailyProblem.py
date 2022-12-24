import abc
import time


class AbstractDailyProblem(abc.ABC):
    def __init__(self, q1_test_answer, q2_test_answer):
        self.__q1_test = q1_test_answer
        self.__q2_test = q2_test_answer

    def parse(self, input_path: str, entry_separator='\n'):
        return list(map(self.parse_entry, open(input_path).read().strip().split(entry_separator)))

    def parse_entry(self, entry: str):
        return entry

    @abc.abstractmethod
    def question_1(self, input_path) -> int:
        pass

    @abc.abstractmethod
    def question_2(self, input_path) -> int:
        pass

    def run(self, test_path="test.txt", input_path="input.txt") -> bool:
        try:
            assert (test_result_1 := self.question_1(test_path)) == self.__q1_test
        except AssertionError:
            print(f"Question 1 fails: expected {self.__q1_test}, found {test_result_1}")
            return False

        t1 = time.time()
        print(f"Answer #1: {self.question_1(input_path)} [{(time.time() - t1)*1000:0.0f}ms]")

        try:
            assert (test_result_2 := self.question_2(test_path)) == self.__q2_test
        except AssertionError:
            print(f"Question 2 fails: expected {self.__q2_test}, found {test_result_2}")
            return False

        t2 = time.time()
        print(f"Answer #2: {self.question_2(input_path)} [{(time.time() - t2)*1000:0.0f}ms]")
        return True
