from AbstractDailyProblem import AbstractDailyProblem


char_to_movement = {
	'v': (1, 0),
	'^': (-1, 0),
	'>': (0, 1),
	'<': (0, -1)
}

class Advent2015day3(AbstractDailyProblem):

	def question_1(self, input_path) -> int:
		i, j = 0, 0
		houses = {(0, 0)}
		for di, dj in map(char_to_movement.get, self.parse(input_path)[0]):
			i += di
			j += dj
			houses.add((i, j))
		return len(houses)

	def question_2(self, input_path) -> int:
		santa_i, santa_j = 0, 0
		robot_i, robot_j = 0, 0
		houses = {(0, 0)}
		move_santa = True
		for di, dj in map(char_to_movement.get, self.parse(input_path)[0]):
			if move_santa:
				santa_i += di
				santa_j += dj
				houses.add((santa_i, santa_j))
			else:
				robot_i += di
				robot_j += dj
				houses.add((robot_i, robot_j))
			move_santa = not move_santa
		return len(houses)

	def __init__(self):
		super().__init__(2, 11)


if __name__ == '__main__':
	Advent2015day3().run('../resources/2015/3/test.txt', '../resources/2015/3/input.txt')
