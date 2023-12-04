#!/usr/bin/env python3

from typing import List

directions = [
	(-1, -1), (-1, 0), (-1, +1),
	( 0, -1),          ( 0, +1),
	(+1, -1), (+1, 0), (+1, +1),
]

schematic = []


def _out_of_bounds(coordinate: List[int], schematic: List[List[int]]) -> bool:
	x, y = coordinate
	max_x = len(schematic)
	max_y = len(schematic[0])
	return (not max_x > x >= 0) or (not max_y > y >= 0)


# Load schematic into memory
for line in open("input.txt").readlines():
	schematic.append(line.strip())

total = 0

# Search for symbols
for i, row in enumerate(schematic):
	for j, value in enumerate(row):
		# If a symbol is found
		if not value.isnumeric() and value != '.':
			searched = set()
			numbers = []
			# Search for associated numbers
			for dx, dy in directions:
				pointer = (i+dx, j+dy)

				# Handle out-of-bounds indexes & those in already found numbers
				if _out_of_bounds(pointer, schematic) or pointer in searched:
					continue
				searched.add(pointer)

				# If a number is found, collect it
				if schematic[pointer[0]][pointer[1]].isnumeric():
					start, end = pointer[1], pointer[1]
					found = set()
					scout = list(pointer)
					
					while found != {"start", "end"}:
						if "start" not in found:
							scout[1] -= 1
						else:
							scout[1] += 1
						
						searched.add(tuple(scout))

						if _out_of_bounds(scout, schematic) or not schematic[scout[0]][scout[1]].isnumeric():
							if "start" not in found:
								found.add("start")
								start = scout[1] + 1
								scout[1] = pointer[1]
							else:
								found.add("end")
								end = scout[1]
					
					if start == end:
						numbers.append(int(schematic[pointer[0]][start]))
					else:
						numbers.append(int(schematic[pointer[0]][start:end]))
			if len(numbers) == 2:
				total += numbers[0] * numbers[1]

print(total)
