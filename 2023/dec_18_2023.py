from AbstractDailyProblem import AbstractDailyProblem


direction_vectors = {
	'U': (-1, 0),
	'D': (1, 0),
	'L': (0, -1),
	'R': (0, 1)
}


def better_instructions(instructions: list[tuple[str, int]]) -> dict[int, list[tuple[int, int]]]:
	"""Instructions as segments (row, col1, col2"""
	parsed_instructions = {}
	cur_x, cur_y = 0, 0
	for direction, distance in instructions:
		dx, dy = direction_vectors[direction]
		new_x = cur_x + dx * distance
		new_y = cur_y + dy * distance
		if dy != 0:
			parsed_instructions.setdefault(new_x, []).append((min(cur_y, new_y), max(cur_y, new_y)))
		cur_x = new_x
		cur_y = new_y
	return parsed_instructions


def get_dig_volume_scan(instructions: list[tuple[str, int]]) -> int:
	volume = 0
	instruction_segments = better_instructions(instructions)
	prev_x = min(instruction_segments.keys()) - 1
	y_list = list(sorted({y for _, segments in instruction_segments.items() for s in segments for y in s}))
	is_active = {(y1, y2): False for y1, y2 in zip(y_list[:-1], y_list[1:])}
	for new_x, segments_in_x in sorted(instruction_segments.items(), key=lambda s: s[0]):
		was_active = {k: v for k, v in is_active.items()}

		# integral volume between xs
		prev_segment_is_active = False
		for (instruction_start, instruction_end), activity in sorted(was_active.items(), key=lambda _: _[0][0]):
			if activity:
				volume += (new_x - prev_x - 1) * (instruction_end - instruction_start + (0 if prev_segment_is_active else 1))
			prev_segment_is_active = activity

		# update segment activity
		for instruction_start, instruction_end in segments_in_x:
			for (segment_start, segment_end), activity in is_active.items():
				if instruction_start <= segment_start and segment_end <= instruction_end:
					is_active[(segment_start, segment_end)] = not activity

		prev_segment_is_active = False
		# count volume on current line
		for (segment_start, segment_end), activity in sorted(is_active.items(), key=lambda _: _[0][0]):
			segment_is_active = activity or was_active[(segment_start, segment_end)]
			if segment_is_active:
				volume += segment_end - segment_start + (0 if prev_segment_is_active else 1)
			prev_segment_is_active = segment_is_active

		prev_x = new_x
	return volume


class Advent2023day18(AbstractDailyProblem):

	def __init__(self) -> None:
		super().__init__(62, 952408144115)

	def parse_entry(self, entry: str) -> tuple[str, int, str]:
		direction, length, color = super().parse_entry(entry).split(' ')
		return direction, int(length), color[1:-1]

	def question_1(self, input_path) -> int:
		dig_plan = self.parse(input_path)
		instructions = [(direction, distance) for direction, distance, _ in dig_plan]
		return get_dig_volume_scan(instructions)

	def question_2(self, input_path) -> int:
		dig_plan = self.parse(input_path)
		code_to_dir = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
		instructions = [(code_to_dir[code[-1]], int(code[1:-1], 16)) for _, _, code in dig_plan]
		return get_dig_volume_scan(instructions)


if __name__ == '__main__':
	Advent2023day18().run('../resources/2023/18/test.txt', '../resources/2023/18/input.txt')
