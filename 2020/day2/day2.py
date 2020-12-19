from re import split


def question1():
    def is_valid_passwd(line: str):
        # lines follow "i-j letter: passwd"
        i, j, letter, passwd = split("-| |: ", line[:-1])
        return int(i) <= passwd.count(letter) <= int(j)

    file = open("input.txt", "r")
    answer = sum(map(is_valid_passwd, file.readlines()))
    print(answer)


def question2():
    def is_valid_passwd(line: str):
        i, j, letter, passwd = split("-| |: ", line[:-1])
        return (passwd[int(i)-1] == letter) ^ (passwd[int(j)-1] == letter)

    file = open("input.txt", "r")
    answer = sum(map(is_valid_passwd, file.readlines()))
    print(answer)


if __name__ == '__main__':
    print("Answer #1:")
    question1()
    print("Answer #2:")
    question2()
