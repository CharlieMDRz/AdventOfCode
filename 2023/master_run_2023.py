import time

from AbstractDailyProblem import time_format

if __name__ == '__main__':
    start_time = time.time_ns()
    for date in range(1, 26):
        try:
            module_name = f"dec_{date}_2023"
            class_name = f"Advent2023day{date}"
            exec(f'from {module_name} import {class_name}')
            test_path = input_path = f"../resources/2023/{date}/test.txt"
            # print(f'Running solution for day {date}')
            time.sleep(0.001)
            vars()[class_name]().question_1(input_path)
            vars()[class_name]().question_2(input_path)
        except Exception:
            print(f'Failed to run day {date}')

    print(time_format(time.time_ns() - start_time))
