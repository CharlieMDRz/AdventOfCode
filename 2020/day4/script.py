def read_input():
    entries = []
    with open("input.txt") as f:
        entry = {}
        for line in f.readlines() + [""]:
            line = line.rstrip()
            if line == "":
                entries.append(entry)
                entry = {}
            else:
                entry.update({arg.split(':')[0]: arg.split(':')[1] for arg in line.split()})

    return entries


def question_1():
    def is_valid_passport(dic: dict):
        required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
        return len(set(dic.keys()).intersection(required_fields)) == len(required_fields)

    passports = read_input()
    return len(list(filter(is_valid_passport, passports)))


def question_2():
    validation = {
        'byr': lambda v: 1920 <= int(v) <= 2002,
        'iyr': lambda v: 2010 <= int(v) <= 2020,
        'eyr': lambda v: 2020 <= int(v) <= 2030,
        'hgt': lambda v: 150 <= int(v[:-2]) <= 193 if v[-2:] == 'cm' else 59 <= int(v[:-2]) <= 76 if v[-2:] == 'in' else False,
        'hcl': lambda v: (v[0] == '#') and (len(v) == 7) and all(47 < ord(c) < 58 or 96 < ord(c) < 103 for c in v[1:]),
        'ecl': lambda v: v in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
        'pid': lambda v: len(v) == 9 and int(v) >= 0,
    }

    def is_valid_passport(dic: dict):
        try:
            return all(validation[key](dic[key]) for key in validation)
        except Exception:
            # Either missing key or false condition, eg cannot convert input to int
            return False

    # TEST
    # passport = {'pid': '087499704', 'hgt': '74in', 'ecl': 'grn', 'iyr': '2012', 'eyr': '2030', 'byr': '1980',
    #             'hcl': '#623a2f'}
    # for key in passport:
    #     print(key, validation[key](passport[key]))
    # print(is_valid_passport(passport))

    passports = read_input()
    return len(list(filter(is_valid_passport, passports)))


if __name__ == '__main__':
    print(question_1())
    print(question_2())
