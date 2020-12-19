def parse_id(ticket_str):
	ticket_int = ticket_str.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1')
	return int(ticket_int, 2)


def question1():
	return max(map(parse_id, open('input.txt').readlines()))


def question2():
	seats = []
	with open('input.txt') as f:
		for line in f.readlines():
			seat_id = parse_id(line)
			row, col = seat_id // 8, seat_id % 8
			if row not in [0, 127]:
				seats.append(seat_id)
	seats.sort()
	for u, v in zip(seats[:-1], seats[1:]):
		if v - u == 2:
			return u + 1


if __name__ == "__main__":
	assert parse_id('BFFFBBFRRR') == 567
	assert parse_id('FFFBBBFRRR') == 119
	assert parse_id('BBFFBBFRLL') == 820
	print("Answer #1: ", question1())
	print("Answer #2: ", question2())
