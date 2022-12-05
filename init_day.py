#!/usr/bin/env python
from pathlib import Path

if __name__ == '__main__':
    import sys
    from os import sep
    print(sys.argv)
    year = '2020' if len(sys.argv) < 3 else sys.argv[2]
    day = sys.argv[1]

    resource_path = f"resources/{year}/{day}"
    Path(resource_path).mkdir(parents=True, exist_ok=True)
    open("{}/input.txt".format(resource_path), "w").close()
    open("{}/test.txt".format(resource_path), "w").close()

    script_path = sep.join([year, ""])
    Path(script_path).mkdir(parents=True, exist_ok=True)
    f = open(f"{script_path}dec_{day}_{year}.py", "w")
    class_name = f"Advent{year}day{day}"
    f.write(f"from AbstractDailyProblem import AbstractDailyProblem\n\n\nclass {class_name}(AbstractDailyProblem):")
    f.write("\n\n\tdef __init__(self):\n\t\tsuper().__init__(0, 0)\n")
    f.write(f"\n\nif __name__ == '__main__':\n\t{class_name}().run()\n")
    f.close()
