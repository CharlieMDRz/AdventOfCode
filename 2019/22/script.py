import re

class CardStack:
	def __init__(self, length = 10007):
		self.l = list(range(length))

	def deal_into(self):
		self.l = list(reversed(self.l))

	def cut(self, n):
		self.l = self.l[n:] + self.l[:n]

	def deal(self, n):
		size = len(self.l)
		target = [0 for _ in range(size)]
		target_pos = 0
		for elt in self.l:
			target[target_pos] = elt
			target_pos = (target_pos + n) % size
		self.l = target

	def __str__(self):
		return str(self.l)

def question1():
	stack = CardStack()
	for line in open('input.txt').readlines():
		if line.startswith('deal into'):
			stack.deal_into()
		elif line.startswith('deal with'):
			inc = int(re.search('increment (-?\d+)', line).group(1))
			stack.deal(inc)
		elif line.startswith('cut'):
			inc = int(re.search('cut (-?\d+)', line).group(1))
			stack.cut(inc)
	return stack.l.index(2019)

def question2():
	return 0

def test():
	stack = CardStack(10)
	print(stack)
	stack.deal_into()
	print(stack)

	stack = CardStack(10)
	print(stack)
	stack.cut(3)
	print(stack)

	stack = CardStack(10)
	print(stack)
	stack.cut(-4)
	print(stack)

	stack = CardStack(10)
	print(stack)
	stack.deal(3)
	print(stack)

if __name__ == "__main__":
	# test()
	print("Answer #1: ", question1())
	print("Answer #2: ", question2())
