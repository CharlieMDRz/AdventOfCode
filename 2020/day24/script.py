coords = {'nw': (-1, 1), 'ne': (1, 1), 'sw': (-1, -1), 'se': (1, -1), 'w': (-2, 0), 'e': (2, 0)}


def neighbours(tile_coords):
	return {(tile_coords[0] + mv0[0], tile_coords[1] + mv0[1]) for mv0 in coords.values()}


def read_input(path):
	def parse_line(_line: str):
		_line = _line.strip()
		cur = 0
		movements = []
		while cur < len(_line):
			if _line[cur] in ['n', 's']:
				new_cur = cur + 2
			else:
				new_cur = cur + 1
			movements.append(_line[cur: new_cur])
			cur = new_cur
		return movements

	instructions = []
	for line in open(path).readlines():
		instructions.append(parse_line(line))
	return instructions


if __name__ == '__main__':
	path, n_days = "input.txt", 100

	tiles = {}
	for v in read_input(path):
		x, y = 0, 0
		for mv in v:
			x += coords[mv][0]
			y += coords[mv][1]
		tile = (x, y)
		if tile not in tiles:
			tiles[tile] = 0
		tiles[tile] = 1 - tiles[tile]

	print("Answer #1: ", sum(tiles.values()))

	tiles = {k for (k, v) in tiles.items() if v == 1}  # only store black tiles

	for _ in range(n_days):
		# print("Day {}: {}".format(_, len(tiles)))  # debug
		black_tiles = set()
		white_tiles = set()
		for tile in tiles:
			for neigh_tile in neighbours(tile).union({tile}):
				if neigh_tile in black_tiles or neigh_tile in white_tiles:
					continue  # already computed, skip
				elif neigh_tile in tiles:
					# neigh_tile is black
					if len(tiles.intersection(neighbours(neigh_tile))) in [1, 2]:
						black_tiles.add(neigh_tile)
					else:
						white_tiles.add(neigh_tile)
				else:
					# neigh_tile is white
					if len(tiles.intersection(neighbours(neigh_tile))) == 2:
						black_tiles.add(neigh_tile)
					else:
						white_tiles.add(neigh_tile)

		tiles = black_tiles

	print("Answer #2: ", len(tiles))
