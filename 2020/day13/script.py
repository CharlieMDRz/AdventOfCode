from numpy import argmin, array


def restart_line():
	import sys
	sys.stdout.write('\r')
	sys.stdout.flush()


def question1():
	l = open('input.txt').readlines()
	min_departure = int(l[0])
	bus_ids = list(map(int, filter(lambda v: v != 'x', l[1].split(','))))
	print(bus_ids)
	best_id = bus_ids[argmin(array(list(map(lambda v: v - (min_departure % v), bus_ids))))]
	print(best_id, min_departure % best_id, min_departure//best_id + 1)
	return best_id * (best_id - (min_departure % best_id))


def question2():
	line = open('input.txt').readlines()[1].split(',')
	bus_ids_pos = list(map(lambda v: (v[0], int(v[1])), filter(lambda v: v[1] != 'x', enumerate(line))))
	# bus_ids_pos = [(0, 7), (1, 13), (4, 59), (6, 31), (7, 19)]  # test entry
	print(bus_ids_pos)

	def euclidean_theorem(a, b):
		"""
		Adapted from https://fr.wikipedia.org/wiki/Algorithme_d%27Euclide_%C3%A9tendu#Pseudo-code
		"""
		r1, u1, v1, r2, u2, v2 = a, 1, 0, b, 0, 1
		while r2 != 0:
			q = r1 // r2
			r1, u1, v1, r2, u2, v2 = r2, u2, v2, r1 - q*r2, u1 - q*u2, v1 - q*v2
		return u1, v1

	prod = 1  # product of all (prime) bus ids
	for b in bus_ids_pos:
		prod *= b[1]

	# Build a satisfying solution from the chinese remainder theorem
	t = 0
	for pos, bus_id in bus_ids_pos:
		rest = prod / bus_id
		t -= (pos % bus_id) * rest * euclidean_theorem(bus_id, rest)[1]

	t = t % prod  # find the smallest positive satisfying solution
	assert all((t+pos) % bid == 0 for pos, bid in bus_ids_pos)
	return t


if __name__ == "__main__":
	print("Answer #1: ", question1())
	from time import time, sleep

	t0 = time()
	print("Answer #2: ", question2())
	print("Solved in {:0.3f} ms".format(1000 * (time() - t0)))
