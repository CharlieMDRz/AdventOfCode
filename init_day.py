#!/usr/bin/env python
from pathlib import Path

if __name__ == '__main__':
    import sys
    from os import sep
    print(sys.argv)
    year = '2020' if len(sys.argv) < 3 else sys.argv[2]
    day = sys.argv[1]
    folder_path = sep.join([year, "day"+day, ""])
    Path(folder_path).mkdir(parents=True, exist_ok=True)
    f = open("{}input.txt".format(folder_path), "w")
    f.close()
    f = open("{}test.txt".format(folder_path), "w")
    f.close()

    class_name = f"Advent{year}_{day}"
    f = open(f"{folder_path}{class_name}.py", "w")
    f.write(f"from AbstractDailyProblem import AbstractDailyProblem\n\n\nclass {class_name}(AbstractDailyProblem):")
    f.write("\n\n\tdef __init__(self):\n\t\tsuper().__init__(0, 0)\n")
    f.write(f"\n\nif __name__ == '__main__':\n\t{class_name}().run()\n")
    f.close()
