#!/usr/bin/env python3

from collections import defaultdict


class FileSystem():
	directories: dict = {}

	def __init__(self, cmd_file: str):
		self.root = Directory(parent=None, name="/")
		self._build_system(self._read_commands(cmd_file))

	@staticmethod
	def _read_commands(filename: str) -> list[str]:
		commands = [line.strip() for line in open(filename).readlines()]
		return commands

	def _build_system(self, commands: list[str]):
		current_dir = '/'

		for command in commands:
			# print(f"Command: {command}")
			if command.startswith("$ cd "):
				next_dir = command[5:]
				previous_dir = current_dir

				if next_dir == '/':
					current_dir = self.root
				elif next_dir == '..':
					current_dir = previous_dir.parent
				else:
					if next_dir in previous_dir.children.keys():
						current_dir = previous_dir.children[next_dir]
					else:
						current_dir = Directory(
							parent=previous_dir,
							name=next_dir,
						)
			elif command.startswith("$ ls"):
				pass
			elif command.startswith("dir "):
				current_dir.add_child(command[4:])
			else:
				size, name = command.strip().split(' ')
				current_dir.add_file(
					name=name,
					size=int(size),
				)

	def solve_a(self) -> int:
		"""Find directories with total size < 100000"""
		sizes = self.root.get_child_sizes()

		# Sum those directory sizes
		total = sum([
			size for name, size in sizes.items()
			if size <= 100000
		])

		return total

	def solve_b(self) -> int:
		"""Find the size of the smallest directory we can delete"""

		space_total = 70000000
		space_needed = 30000000

		space_used = self.root.get_size()
		space_unused = space_total - space_used

		space_to_free = space_needed - space_unused
		# print(f"Need to find: {space_to_free}")

		# Find minimum value of dir above space_to_free
		candidates = {
			directory: size for directory, size in self.root.get_child_sizes().items()
			if size > space_to_free
		}

		return min(candidates.values())


class Directory():
	def __init__(self, parent, name: str):
		self.parent = parent
		self.name = name
		self.full_path = '/' if self.parent is None else f"{self.parent.full_path}{'/' if self.parent.full_path != '/' else ''}{self.name}"
		self.children: dict[Directory] = {}
		self.files: dict[File] = {}

	def get_size(self):
		size_local = sum(self.files.values())
		size_children = sum([child.get_size() for child in self.children.values()])
		return size_local + size_children

	def get_child_sizes(self) -> dict[int]:
		sizes = {self.full_path: self.get_size()}
		for name, obj in self.children.items():
			sizes = sizes | obj.get_child_sizes()
		return sizes

	def add_child(self, name: str):
		self.children[name] = Directory(parent=self, name=name)

	def add_file(self, name: str, size: int):
		self.files[name] = size
		# self.files[name] = File(name=name, size=size)

	def view(self, depth: int = 0):
		print(f"{' '*depth}- {self.name} (dir, size={self.get_size()})")
		for child in self.children.values():
			child.view(depth=depth+1)
		for file_name, file_size in self.files.items():
			print(f"{' '*(depth+1)}- {file_name} (file, size={file_size})")


class File(dict):
	def __init__(self, name: str, size: int):
		self.name: str = name
		self.size: int = size


if __name__ == '__main__':
	fs = FileSystem("input.txt")
	# print(fs.root.get_size())
	# fs.root.view()
	print(f"A: {fs.solve_a()}")
	print(f"B: {fs.solve_b()}")
