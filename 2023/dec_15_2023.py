import functools

from AbstractDailyProblem import AbstractDailyProblem


def HASH(inst: str):
	v = 0
	for char in inst:  # type: str
		code = ord(char)
		v = (v + code) * 17 % 256
	return v


def process_sub(boxes, label):
	box = boxes[HASH(label)]
	for i, (lens_label, _) in enumerate(box):
		if label == lens_label:
			box.pop(i)
			return


def process_eq(boxes, lens_label, lens_focus):
	box = boxes[HASH(lens_label)]
	lens_focus = int(lens_focus)
	for i in range(len(box) + 1):
		if i == len(box):
			box.append((lens_label, lens_focus))
		elif box[i][0] == lens_label:
			box[i] = lens_label, lens_focus
			return


class Advent2023day15(AbstractDailyProblem):

	def __init__(self):
		super().__init__(1320, 145)

	def question_1(self, input_path) -> int:
		instructions = self.parse(input_path, ',')
		return sum(map(HASH, instructions))

	def question_2(self, input_path) -> int:
		instructions = self.parse(input_path, ',')
		boxes = [[] for _ in range(256)]
		for i in instructions:
			if '=' in i:
				process_eq(boxes, *i.split('='))
			elif '-' in i:
				process_sub(boxes, i[:-1])

		res = 0
		for box_index, box in enumerate(boxes):
			for lens_index, (_, lens_focal) in enumerate(box):
				res += (box_index + 1) * (lens_index + 1) * lens_focal
		return res


if __name__ == '__main__':
	Advent2023day15().run('../resources/2023/15/test.txt', '../resources/2023/15/input.txt')
