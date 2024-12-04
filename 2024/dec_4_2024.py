from AbstractDailyProblem import AbstractDailyProblem


def has_word_in_pos_dir(grid, word, i, j, di, dj):
	if not word:
		return True
	elif not (0 <= i < len(grid) and 0 <= j < len(grid[0])):
		return False
	else:
		return grid[i][j] == word[0] and has_word_in_pos_dir(grid, word[1:], i+di, j+dj, di, dj)


def word_occurences_from_pos(grid, word, i, j) -> int:
	directions = [(di, dj) for di in range(-1, 2) for dj in range(-1, 2) if di or dj]
	return sum(has_word_in_pos_dir(grid, word, i, j, *dir_vec) for dir_vec in directions)


class Advent2024day4(AbstractDailyProblem):

	def __init__(self):
		super().__init__(18, 9)

	def question_1(self, input_path) -> int:
		grid = self.parse(input_path)
		result = sum(word_occurences_from_pos(grid, 'XMAS', i, j) for i in range(len(grid)) for j in range(len(grid[0])))
		return result


	def question_2(self, input_path) -> int:
		grid = self.parse(input_path)
		result = 0
		for i in range(1, len(grid)-1):
			for j in range(1, len(grid[0])-1):
				found_x_mas = grid[i][j] == 'A' and {grid[i-1][j-1], grid[i+1][j+1]} == {'M', 'S'} and {grid[i-1][j+1], grid[i+1][j-1]} == {'M', 'S'}
				result += int(found_x_mas)
		return result



if __name__ == '__main__':
	Advent2024day4().run('../resources/2024/4/test.txt', '../resources/2024/4/input.txt')
