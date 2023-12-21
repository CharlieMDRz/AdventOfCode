from AbstractDailyProblem import AbstractDailyProblem


def display(pattern: list[str]):
	print('\n'.join(pattern + ['']))


def row_sym_score(pattern: list[str]) -> int:
	for symmetry_index in range(1, len(pattern)):
		left_index, right_index = symmetry_index-1, symmetry_index
		while pattern[left_index] == pattern[right_index]:
			left_index -= 1
			right_index += 1

			if left_index < 0 or right_index >= len(pattern):
				return symmetry_index
	return 0


def col_sym_score(pattern: list[str]) -> int:
	pattern = [''.join(_[j] for _ in pattern) for j in range(len(pattern[0]))]
	return row_sym_score(pattern)


def diff(first: str, second: str) -> list[int]:
	return [i for i, (first_char, second_char) in enumerate(zip(first, second)) if first_char != second_char]


def find_smudge(pattern: list[str]) -> tuple[int, int]:
	def find_row_smudge(_p):
		for row_sym_index in range(1, len(_p)):
			left_index, right_index = row_sym_index - 1, row_sym_index
			while 0 <= left_index and right_index < len(_p):
				left_pattern = _p[left_index]
				right_pattern = _p[right_index]
				patterns_diff = diff(left_pattern, right_pattern)
				if len(patterns_diff) > 1:
					break
				if len(patterns_diff) == 1:
					return left_index, patterns_diff[0]
				left_index -= 1
				right_index += 1
		return None

	row_smudge = find_row_smudge(pattern)
	if row_smudge:
		return row_smudge
	else:
		pattern = [''.join(_[j] for _ in pattern) for j in range(len(pattern[0]))]
		i, j = find_row_smudge(pattern)
		return j, i


def clean_smudge(pattern: list[str]) -> list[str]:
	i, j = find_smudge(pattern)
	cloned_pattern = list(map(str, pattern))
	cloned_pattern[i] = ''.join({'.': '#', '#': '.'}[v] if j1 == j else v for j1, v in enumerate(pattern[i]))
	return cloned_pattern


class Advent2023day13(AbstractDailyProblem):

	def __init__(self):
		super().__init__(405, 400)

	def parse_entry(self, entry: str):
		return [_.strip() for _ in entry.strip().split('\n')]

	def question_1(self, input_path) -> int:
		patterns = self.parse(input_path, '\n\n')
		return 100 * sum(map(row_sym_score, patterns)) + sum(map(col_sym_score, patterns))

	def question_2(self, input_path) -> int:
		patterns = self.parse(input_path, '\n\n')
		res = 0
		for p in patterns:
			h_score = row_sym_score(p)
			v_score = col_sym_score(p)
			display(p)
			print(find_smudge(p))
			p = clean_smudge(p)
			display(p)
			h_score_clean = row_sym_score(p)
			v_score_clean = col_sym_score(p)
			if h_score and h_score == h_score_clean:
				res += v_score_clean
			elif v_score and v_score == v_score_clean:
				res += 100 * h_score_clean
			else:
				res += v_score_clean
				res += 100 * h_score_clean

		return res


if __name__ == '__main__':
	Advent2023day13().run('../resources/2023/13/test.txt', '../resources/2023/13/input.txt')
