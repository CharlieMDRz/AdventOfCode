class Item:
	def __init__(self, value, next=None):
		self.value = value
		self.next = next

	def __str__(self):
		return "{} -> {}".format(self.value, "None" if self.next is None else self.next.value)


class Queue:

	def __init__(self, values: list):
		self.head = None  # type: Item
		self.__items = [None for _ in range(max(values)+1)]  # type: list

		prev = None  # type: Item
		for _ in values:
			self.__items[_] = Item(_)
			if prev is not None:
				prev.next = self[_]
			prev = self[_]

		self[values[-1]].next = self[values[0]]
		self.head = self[values[0]]

	def __getitem__(self, item: int) -> Item:
		return self.__items[item]

	def __str__(self):
		if self.head is None:
			return "[]"
		res = "[{}".format(self.head.value)
		item = self.head.next
		while item.value != self.head.value:
			res += ", {}".format(item.value)
			item = item.next
		return res + "]"


def question1(input_items, n_moves, q2=False):
	cups_items = list(map(int, [_ for _ in str(input_items)]))
	if q2:
		cups_items += range(max(cups_items)+1, 1000001)
	m, M = min(cups_items), max(cups_items)

	cups = Queue(cups_items)

	from time import time
	t0 = time()
	cur_cup = cups[cups_items[0]]  # type: Item
	for _ in range(n_moves):
		buf_list = [cur_cup.next, cur_cup.next.next, cur_cup.next.next.next]  # 3 values following the current cup
		buf_val = [_.value for _ in buf_list]

		target_lbl = cur_cup.value - 1
		while target_lbl in buf_val or target_lbl < m:
			target_lbl -= 1
			if target_lbl < m:
				target_lbl = M

		split_cup = cups[target_lbl]
		cur_cup.next = buf_list[-1].next
		buf_list[-1].next = split_cup.next
		split_cup.next = buf_list[0]
		cur_cup = cur_cup.next

	if q2:
		item = cups[1]
		v1, v2 = item.next.value, item.next.next.value
		print(time()-t0, (time()-t0)/n_moves)
		return v1, v2, v1 * v2
	else:
		cups.head = cups[1]
		print(time()-t0, "seconds")
		return cups


if __name__ == "__main__":
	test = 389125467
	input1 = 463528179
	print("Answer #1: ", question1(test, 100))
	print("Answer #2: ", question1(input1, 10**7, True))
