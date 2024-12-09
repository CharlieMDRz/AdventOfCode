import collections

import tqdm

from AbstractDailyProblem import AbstractDailyProblem

class FileSystem:
	index_map: list[int]
	free_space_indexes: list[int]
	free_space_at_index: dict[int, int]

	def __init__(self, disk_map: list[int]):
		self.index_map = [None] * sum(disk_map)
		self.free_space_at_index = {}
		self.free_space_indexes = []

		id_number = 0
		processing_file = True
		file_index = 0
		for block_size in disk_map:
			if processing_file:
				self.index_map[file_index:(file_index+block_size)] = [id_number] * block_size
				id_number += 1
			else:
				self.free_space_indexes.append(file_index)
				self.free_space_at_index[file_index] = block_size
			processing_file = not processing_file
			file_index += block_size

	def __len__(self):
		return len(self.index_map)

	def __getitem__(self, item):
		return self.index_map[item]

	@property
	def files(self) -> list[tuple[int, int, int]]:
		res = []
		for index, file_index in enumerate(self.index_map):
			if file_index:
				if res and res[-1][0] == file_index:
					res[-1][2] += 1  # increase size
				else:
					res.append([file_index, index, 1])
		return res

	def leftmost_index_of_size(self, min_size: int) -> int:
		return next(
			mem_index for mem_index in self.free_space_indexes
			if self.free_space_at_index[mem_index] >= min_size
		)

	def move(self, source, target, size) -> None:
		self.index_map[target: (target+size)] = self.index_map[source: (source+size)]
		self.index_map[source: (source+size)] = [None] * size

		filled_space_index = self.free_space_indexes.index(target)
		if self.free_space_at_index[target] > size:
			# partly filled space
			self.free_space_at_index[target+size] = self.free_space_at_index[target] - size
			self.free_space_indexes[filled_space_index] = target+size
		else:
			# fully filled space
			self.free_space_indexes.pop(filled_space_index)
		del self.free_space_at_index[target]


def check_sum(file_system: list[int]) -> int:
	return sum((index * value if value else 0) for index, value in enumerate(file_system))


def update(file_system: list[int]) -> None:
	value_to_store = file_system.pop(-1)
	new_pos = next(i for i, v in enumerate(file_system) if v is None)
	file_system[new_pos] = value_to_store


class Advent2024day9(AbstractDailyProblem):

	def __init__(self):
		super().__init__(1928, 2858)

	def parse_entry(self, entry: str):
		disk_map = list(map(int, super().parse_entry(entry)))
		return FileSystem(disk_map)

	def question_1(self, input_path) -> int:
		file_system: FileSystem = self.parse(input_path)[0]
		while None in file_system.index_map:
			index = file_system.leftmost_index_of_size(1)
			file_system.move(len(file_system) - 1, index, 1)
			while file_system[-1] is None:
				file_system.index_map.pop(-1)
		return check_sum(file_system.index_map)

	def question_2(self, input_path) -> int:
		file_system: FileSystem = self.parse(input_path)[0]
		for _, start_index, file_size in reversed(file_system.files):
			try:
				new_index = file_system.leftmost_index_of_size(file_size)
				if new_index < start_index:
					file_system.move(start_index, new_index, file_size)
			except StopIteration:
				continue
		return check_sum(file_system.index_map)


if __name__ == '__main__':
	Advent2024day9().run('../resources/2024/9/test.txt', '../resources/2024/9/input.txt')
