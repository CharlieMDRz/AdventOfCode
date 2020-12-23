from enum import Enum
from itertools import product
from math import sqrt
from typing import Dict, List

from numpy import array, full, prod, rot90, flip, ndarray


class Direction(Enum):
	Top = "T"
	Left = "L"
	Bottom = "B"
	Right = "R"

	def __neg__(self):
		opposite = {Direction.Top: Direction.Bottom, Direction.Bottom: Direction.Top,
					Direction.Left: Direction.Right, Direction.Right: Direction.Left}
		return opposite[self]

	def __hash__(self):
		return hash(self.value)


class JigsawPiece:

	def __init__(self, pid, image):
		self.id = pid
		self.pat = image
		self.enc = {}
		self.neighbour = {}
		self.build_border_encoding()

	def build_border_encoding(self):
		def encode(_border):
			e1, e2 = 0, 0
			for b1, b2 in zip(_border, reversed(_border)):
				e1 += b1
				e2 += b2
				e1 <<= 1
				e2 <<= 1
			return min(e1, e2)

		# pat = self.pat
		# for border, label in zip([pat[0, :], pat[:, 0], pat[-1, :], pat[:, -1]], ["T", "L", "B", "R"]):
		# 	self.enc[label] = encode(border)
		for _dir in Direction:
			self.enc[_dir] = encode(self[_dir])

	def rotate(self):
		self.pat = rot90(self.pat)
		for new_key, value in zip([Direction.Left, Direction.Bottom, Direction.Right, Direction.Top],
								  [_ for _ in self.enc.values()]):
			self.enc[new_key] = value

	def __getitem__(self, item) -> ndarray:
		if item == Direction.Top:
			return self.pat[0, :]
		if item == Direction.Left:
			return self.pat[:, 0]
		if item == Direction.Bottom:
			return self.pat[-1, :]
		if item == Direction.Right:
			return self.pat[:, -1]

	def flip(self, direction: Direction):
		assert isinstance(direction, Direction)
		if direction in [Direction.Top, Direction.Bottom]:
			self.pat = flip(self.pat, 1)  # flip columns
			self.enc[Direction.Left], self.enc[Direction.Right] = self.enc[Direction.Right], self.enc[Direction.Left]
		else:
			self.pat = flip(self.pat, 0)  # flip lines
			self.enc[Direction.Top], self.enc[Direction.Bottom] = self.enc[Direction.Bottom], self.enc[Direction.Top]


def read_pieces(path):
	_pieces = {}
	for chunk in open(path).read().split("\n\n"):
		lines = chunk.split("\n")
		header = lines.pop(0)
		pid = int(header[5:-1])
		image = array([list(map(lambda c: int(c == '#'), [c for c in line])) for line in lines])
		# print(chunk, "\n", pid, "\n", pattern)
		_pieces[pid] = JigsawPiece(pid, image)
	return _pieces


# It is assumed that the jigsaw is composed of size x size pieces, and that each intersection of two pieces of the
# jigsaw is unique. Consequently, corner pieces can be identified as the 4 pieces which have 2 unique sides
if __name__ == "__main__":
	from time import time
	t0 = time()
	pieces = read_pieces("input.txt")  # type: Dict[int, JigsawPiece]

	size, piece_size = int(sqrt(len(pieces))), 8  # type: int, int
	# First, identify the sides of the pieces. Each side is encoded in a way that is stable through rotation and flip
	encoding_mem = {}  # type: Dict[int, List[int]]
	for p in pieces.values():
		for e in p.enc.values():
			encoding_mem[e] = [p.id] if e not in encoding_mem else encoding_mem[e] + [p.id]

	# Gets corner ids as pieces whose the sum of occurrences of their sides in the pieces is 6
	corners = list(filter(lambda pid: sum(sorted(len(encoding_mem[e1]) for e1 in pieces[pid].enc.values())) == 6, pieces))
	t1 = time()
	print("Answer 1", corners, prod(corners), t1 - t0)

	jigsaw, habitat = full((size, size), 0), full((size*piece_size, size*piece_size), 0)  # type: array, array

	for i, j in product(range(size), range(size)):
		# Find each piece of the jigsaw in an ordered fashion, starting from a corner
		if (i == 0) and (j == 0):
			piece = pieces[corners[0]]  # type: JigsawPiece
			while not len(encoding_mem[piece.enc[Direction.Top]]) * len(encoding_mem[piece.enc[Direction.Left]]) == 1:
				piece.rotate()
		else:
			# Looking for the side matching top or left to the piece at i, j, based on the pieces already placed
			prev_piece_id = jigsaw[i - 1, 0] if j == 0 else jigsaw[i, j - 1]
			match_dir = Direction.Top if j == 0 else Direction.Left  # type: Direction # in which direction is the previous piece
			prev_enc = pieces[prev_piece_id].enc[-match_dir]  # type: int
			piece = pieces[encoding_mem[prev_enc][0]]  # type: JigsawPiece

			# Rotating the piece until the searched encoding faces the good direction
			while piece.enc[match_dir] != prev_enc:
				piece.rotate()

			# final operation, flip the piece if the two facing sides don't match
			if not all(pieces[prev_piece_id][-match_dir] == piece[match_dir]):
				piece.flip(match_dir)

		jigsaw[i, j] = piece.id
		habitat[(piece_size*i):(piece_size*(i+1)), (piece_size*j):(piece_size*(j+1))] = piece.pat[1:-1, 1:-1]
		# remove the newly placed piece from the encoding memory
		for _ in piece.enc.values():
			encoding_mem[_].remove(piece.id)

	size = habitat.shape[0]

	pattern = array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
					 [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
					 [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]])
	target = pattern.sum()

	# Brute force all rotations and flips of the pattern
	for i1 in range(2):
		pattern = flip(pattern, axis=0)
		for i2 in range(4):
			pattern = rot90(pattern)
			sx, sy = pattern.shape
			# if it is found once, discount it on all positions, count remaining #, assumes that patterns don't overlap
			if any((habitat[x:(x+sx), y:(y+sy)] * pattern).sum() == target for x, y in product(range(size-sx), range(size-sy))):
				for x, y in product(range(size-sx), range(size-sy)):
					if (habitat[x:(x+sx), y:(y+sy)] * pattern).sum() == target:
						habitat[x:(x + sx), y:(y + sy)] -= pattern
				print("Answer 2", (habitat > 0).sum(), time() - t1)
				exit()
