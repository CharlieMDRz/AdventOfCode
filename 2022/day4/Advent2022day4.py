from AbstractDailyProblem import AbstractDailyProblem


class Advent2022day4(AbstractDailyProblem):

	def __init__(self):
		super().__init__(2, 4)

	def parse_entry(self, entry):
		return [[int(e) for e in sec.split('-')] for sec in entry.split(',')]

	def question_1(self, input_path) -> int:
		def fully_overlapped(pair1, pair2):
			if pair1[0] < pair2[0]:
				return pair1[1] >= pair2[1]
			elif pair1[0] == pair2[0]:
				return True
			return fully_overlapped(pair2, pair1)

		return len([_ for _ in self.parse(input_path) if fully_overlapped(*_)])

	def question_2(self, input_path) -> int:

		def overlaps_at_all(pair1, pair2):
			return not (pair1[1] < pair2[0] or pair2[1] < pair1[0])
		return len([_ for _ in self.parse(input_path) if overlaps_at_all(*_)])


if __name__ == '__main__':
	Advent2022day4().run()
