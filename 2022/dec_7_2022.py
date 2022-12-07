from typing import Dict, List

from AbstractDailyProblem import AbstractDailyProblem


class File:
	def __init__(self, name: str, size: int):
		self.name = name
		self.__size = size

	@property
	def size(self) -> int:
		return self.__size

	def print(self, indent):
		print('\t' * indent + f"- {self.name} (file, size={self.size})")


class Folder(File):
	__content: Dict[str, File]

	def __init__(self, name: str, parent: File):
		super().__init__(name, 0)
		self.parent = parent
		self.__content = dict()

	def register(self, file: File):
		self.__content[file.name] = file

	def print(self, indent):
		print('\t' * indent + f"- {self.name} (dir)")
		for child_name in sorted(self.__content.keys()):
			self.__content[child_name].print(indent+1)

	@property
	def size(self) -> int:
		return sum(_.size for _ in self.__content.values())

	@property
	def children(self):
		return self.__content.values()

	@property
	def sub_folders(self) -> List[File]:
		res = [self]
		for child in self.children:
			if isinstance(child, Folder):
				res.extend(child.sub_folders)
		return res

	def __getitem__(self, item: str) -> File:
		return self.__content[item]


class Advent2022day7(AbstractDailyProblem):

	def parse(self, input_path, entry_separator='$'):
		commands: List[List[str]] = super().parse(input_path, entry_separator)
		root = Folder('/', None)
		current_folder: Folder = root
		for cmd in commands:
			if cmd[0].startswith('cd'):
				target_folder = cmd[0][3:]
				if target_folder == '..':
					current_folder = current_folder.parent
				elif target_folder == '/':
					current_folder = root
				else:
					current_folder = current_folder[target_folder]
			elif cmd[0].startswith('ls'):
				for content in cmd[1:]:
					attribute, name = content.split(' ')
					if attribute == 'dir':
						current_folder.register(Folder(name, current_folder))
					else:
						current_folder.register(File(name, int(attribute)))

		return root

	def parse_entry(self, entry: str):
		return [cmd_line.strip() for cmd_line in entry.strip().split('\n')]

	def question_1(self, input_path) -> int:
		storage = self.parse(input_path)
		return sum(folder.size for folder in storage.sub_folders if folder.size <= 100000)

	def question_2(self, input_path) -> int:
		storage = self.parse(input_path)
		space_to_free = storage.size - 40000000
		return min(folder.size for folder in storage.sub_folders if folder.size >= space_to_free)

	def __init__(self):
		super().__init__(95437, 24933642)


if __name__ == '__main__':
	Advent2022day7().parse('../resources/2022/7/test.txt').print(0)
	Advent2022day7().run('../resources/2022/7/test.txt', '../resources/2022/7/input.txt')
