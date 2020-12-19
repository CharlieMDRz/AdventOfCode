class Boat:
	card_dir = {'E': (1, 0), 'S': (0, 1), 'W': (-1, 0), 'N': (0, -1)}

	def __init__(self, dirx, diry):
		self.dirx = dirx
		self.diry = diry
		self.posx = 0
		self.posy = 0

	def exec_line(self, line):
		comm, dist = line[0], int(line[1:])
		if comm	in self.card_dir.keys():
			dirx, diry = self.card_dir[comm]
			self.posx += dirx * dist
			self.posy += diry * dist
		elif comm in {'L', 'R'}:
			for _ in range(dist // 90):
				if comm == 'L':
					self.dirx, self.diry = self.diry, -self.dirx
				else:
					self.dirx, self.diry = -self.diry, self.dirx
		elif comm == 'F':
			self.posx += self.dirx * dist
			self.posy += self.diry * dist

	def exec_line_v2(self, line):
		comm, dist = line[0], int(line[1:])
		if comm in self.card_dir.keys():
			dirx, diry = self.card_dir[comm]
			self.dirx += dirx * dist
			self.diry += diry * dist
		elif comm in {'L', 'R'}:
			for _ in range(dist // 90):
				if comm == 'L':
					self.dirx, self.diry = self.diry, -self.dirx
				else:
					self.dirx, self.diry = -self.diry, self.dirx
		elif comm == 'F':
			self.posx += self.dirx * dist
			self.posy += self.diry * dist


def question1():
	ferry = Boat(1, 0)
	for line in open('input.txt').readlines():
		# print(line.strip())
		ferry.exec_line(line.strip())
		# print(ferry.dirx, ferry.diry, ferry.posx, ferry.posy)
	return abs(ferry.posx) + abs(ferry.posy)


def question2():
	ferry = Boat(10, -1)
	for line in open('input.txt').readlines():
		# print(line.strip())
		ferry.exec_line_v2(line.strip())
		# print(ferry.dirx, ferry.diry, ferry.posx, ferry.posy)
	return abs(ferry.posx) + abs(ferry.posy)


if __name__ == "__main__":
	print("Answer #1: ", question1())
	print("Answer #2: ", question2())
