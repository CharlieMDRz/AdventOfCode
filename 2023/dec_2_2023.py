from AbstractDailyProblem import AbstractDailyProblem


class Advent2023day2(AbstractDailyProblem):



	def parse_entry(self, entry: str) -> list[dict[str, int]]:
		return [
			{
				color: int(count)
				for count, color in map(lambda _: _.split(' '), reveal.strip().split(', '))
			}
			for reveal in entry.split(': ')[1].split(';')
		]

	def question_1(self, input_path) -> int:
		games = self.parse(input_path)
		def is_feasible(game: list[dict[str, int]], capacity: dict[str, int]) -> bool:
			for reveal in game:
				for color, count in reveal.items():
					if count > capacity[color]:
						return False
			return True

		return sum(index + 1 for index, game in enumerate(games) if is_feasible(game, {'red': 12, 'green': 13, 'blue': 14}))

	def question_2(self, input_path) -> int:
		games = self.parse(input_path)
		def game_power(game: list[dict[str, int]]):
			max_count = {
				color: max(reveal.get(color, 0) for reveal in game)
				for color in ('red', 'green', 'blue')
			}

			res = 1
			for count in max_count.values():
				res *= count

			return res

		return sum(map(game_power, games))

	def __init__(self):
		super().__init__(8, 2286)


if __name__ == '__main__':
	Advent2023day2().run('../resources/2023/2/test.txt', '../resources/2023/2/input.txt')
