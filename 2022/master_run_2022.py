import time

from AbstractDailyProblem import time_format

if __name__ == '__main__':
    start_time = time.time_ns()
    for date in range(5, 24):
        try:
            module_name = f"dec_{date}_2022"
            class_name = f"Advent2022day{date}"
            exec(f'from {module_name} import {class_name}')
            test_path = input_path = f"../resources/2022/{date}/test.txt"
            print(f'Running solution for day {date}')
            time.sleep(0.001)
            vars()[class_name]().run(test_path, input_path)
        except Exception:
            print('Failed to run')

    print(time_format(time.time_ns() - start_time))
