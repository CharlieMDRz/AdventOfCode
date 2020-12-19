#!/usr/bin/env python

if __name__ == '__main__':
    import sys
    from os import mkdir, sep
    print(sys.argv)
    year = '2020' if len(sys.argv) < 3 else sys.argv[2]
    day = sys.argv[1]
    folder_path = sep.join([year, "day"+day, ""])
    mkdir(folder_path)
    f = open("{}input.txt".format(folder_path), "w")
    f.close()

    f = open("{}script.py".format(folder_path), "w")
    f.write("def question1():\n\treturn 0\n\n\ndef question2():\n\treturn 0\n\n")
    f.write('if __name__ == "__main__":\n\tprint("Answer #1: ", question1())\n\tprint("Answer #2: ", question2())\n')
    f.close()
