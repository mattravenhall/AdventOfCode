#!/usr/bin/env python3

import math
import re


class SandSimulator:
	def __init__(self, filename: str):
		self.source = (500, 0)
		self.rocks: set[tuple[int, int]] = self._build(filename)
		self.sand: set[tuple[int, int]] = set()
		self.range_x = (
			min(min(self.rocks, key=lambda x: x[0])[0], self.source[0]),
			max(max(self.rocks, key=lambda x: x[0])[0], self.source[0])+1,
		)
		self.range_y = (
			min(min(self.rocks, key=lambda x: x[1])[1], self.source[1]),
			max(max(self.rocks, key=lambda x: x[1])[1], self.source[1])+1,
		)

	def _build(self, filename: str) -> set[tuple[int, int]]:
		lines = self._parse_file(filename)
		rocks = self._parse_lines(lines)
		return rocks

	@staticmethod
	def _parse_file(filename: str) -> list[list[tuple[int, int]]]:
		lines = []
		for line in open(filename).readlines():
			line = line.strip()

			points = [tuple(point.split(',')) for point in re.findall(r"\d+,\d+", line)]
			lines.append(points)
		return lines

	@staticmethod
	def _parse_lines(lines: list[list[tuple[int, int]]]):
		rocks = set()
		for line in lines:
			for start, end in zip(line, line[1:]):
				x_range = (
					min(int(start[0]), int(end[0])),
					max(int(start[0]), int(end[0]))+1
				)
				y_range = (
					min(int(start[1]), int(end[1])),
					max(int(start[1]), int(end[1]))+1
				)

				for x in range(*x_range):
					for y in range(*y_range):
						rocks.add((x, y))
		return rocks

	def visualise(self, floor: int = None) -> None:
		if floor is not None:
			range_x = (self.source[0]-30, self.source[0]+30)
			range_y = (self.range_y[0], floor+1)
		else:
			range_x = self.range_x
			range_y = self.range_y

		for y in range(*range_y):
			row = f"[{y}]{' ' * (len(str(range_y[1]))-len(str(y)))}"
			for x in range(*range_x):
				if (x, y) in self.rocks:
					row += '#'
				elif (x, y) in self.sand:
					row += 'o'
				elif (x, y) == self.source:
					row += '+'
				elif y == floor:
					row += '@'
				else:
					row += '.'
			print(row)

	def _falling_sand(self, position: tuple[int, int]) -> None:
		pass

	def simulate(self, visualise: bool = False, floor: int = math.inf) -> None:
		self.sand = set()
		# Default floor is the max y coordinate
		out_of_bounds = self.range_y[1] if floor is math.inf else floor

		completed = False
		while not completed:
			not_air: set[tuple[int, int]] = self.rocks | self.sand | {self.source}

			if visualise:
				print('------')
				self.visualise(floor=floor)

			# Spawn sand from source
			current = self.source
			falling = True
			while falling:
				# Check space below current
				beneath = (current[0], current[1]+1)

				if beneath[1] == floor:
					# Sand has hit the floor
					self.sand.add(current)
					falling = False
				elif beneath[1] >= out_of_bounds:
					# Sand is falling out of bounds
					completed = True
					falling = False
				elif beneath in not_air:
					# print("Above something")
					if (beneath[0]-1, beneath[1]) not in not_air:
						# Checking down-left
						current = beneath[0]-1, beneath[1]
					elif (beneath[0]+1, beneath[1]) not in not_air:
						# Checking down-right
						current = beneath[0]+1, beneath[1]
					else:
						# No longer falling
						falling = False
						if current == self.source:
							# Source is blocked
							completed = True
						# Rest at current location
						self.sand.add(current)
				else:
					# Keep falling if in air
					current = beneath
		if visualise:
			print('------')
			self.visualise(floor=floor)

	def solveA(self) -> int:
		self.simulate()
		return len(self.sand)

	def solveB(self):
		self.simulate(floor=self.range_y[1]+1)#, visualise=True)
		return len(self.sand)


if __name__ == '__main__':
	test_simulator = SandSimulator("test.txt")
	assert test_simulator.solveA() == 24
	assert test_simulator.solveB() == 93

	problem_simulator = SandSimulator("input.txt")
	print(f"A: {problem_simulator.solveA()}")
	print(f"B: {problem_simulator.solveB()}")
