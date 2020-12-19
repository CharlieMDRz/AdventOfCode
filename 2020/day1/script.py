from itertools import product

def question1():
	data = list(map(lambda v: int(v.strip()), open('input.txt').readlines()))
	return next(map(lambda u: u[0] * u[1], filter(lambda u: u[0] + u[1] == 2020, product(data, data))))

def question2():
	data = list(map(lambda v: int(v.strip()), open('input.txt').readlines()))
	return next(map(lambda u: u[0] * u[1] * u[2], filter(lambda u: u[0] + u[1] + u[2] == 2020, product(data, data, data))))

if __name__ == "__main__":
	print("Answer #1: ", question1())
	print("Answer #2: ", question2())
