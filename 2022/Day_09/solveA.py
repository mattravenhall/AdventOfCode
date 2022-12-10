#!/usr/bin/env python3.10

from copy import copy


def gap_exists(pos_head: list[int], pos_tail: list[int]) -> bool:
	"""Check whether tail is far enough away to move"""
	gap_x = abs(pos_head[0] - pos_tail[0])
	gap_y = abs(pos_head[1] - pos_tail[1])

	return True if gap_x > 1 or gap_y > 1 else False


def view_trail(trail: set[tuple[int]], head: list[int], tail: list[int]) -> None:
	max_x, max_y = 6, 6
	min_x, min_y = 0, 0

	for x, y in trail:
		if x > max_x:
			max_x = x
		if y > max_y:
			max_y = y
		if x < min_x:
			min_x = x
		if y < min_y:
			min_y = y

	for y in range(min_y, max_y+1)[::-1]:
		row = []
		for x in range(min_x, max_x+1):
			if [x, y] == head:
				row.append('H')
			elif [x, y] == tail:
				row.append('T')
			elif (x, y) in trail:
				row.append('#')
			else:
				row.append('.')
		print(' '.join(row))
		

def solveA(filename: str) -> set[tuple]:
	visited: set[tuple] = {(0, 0)}

	pos_head: list[int] = [0, 0]
	pos_tail: list[int] = [0, 0]
	orig_tail: list[int] = copy(pos_tail)

	for command in open(filename).readlines():
		trail = set()

		# Move head-tail pair
		match command.strip().split():
			case ["U", distance]:
				pos_head[1] += int(distance)
				if gap_exists(pos_head, orig_tail):
					pos_tail = [pos_head[0], pos_head[1]-1]
					trail = set([(pos_head[0], y+1) for y in range(orig_tail[1], pos_tail[1])])
			case ["D", distance]:
				pos_head[1] -= int(distance)
				if gap_exists(pos_head, orig_tail):
					pos_tail = [pos_head[0], pos_head[1]+1]
					trail = set([(pos_head[0], y) for y in range(pos_tail[1], orig_tail[1])])
			case ["L", distance]:
				pos_head[0] -= int(distance)
				if gap_exists(pos_head, orig_tail):
					pos_tail = [pos_head[0]+1, pos_head[1]]
					trail = set([(x, pos_head[1]) for x in range(pos_tail[0], orig_tail[0])])
			case ["R", distance]:
				pos_head[0] += int(distance)
				if gap_exists(pos_head, orig_tail):
					pos_tail = [pos_head[0]-1, pos_head[1]]
					trail = set([(x+1, pos_head[1]) for x in range(orig_tail[0], pos_tail[0])])
			case _:
				breakpoint()

		visited = visited | trail
		orig_tail = copy(pos_tail)

	return visited


if __name__ == '__main__':
	assert solveA("test.txt") == {
                        (2, 4), (3, 4),
                                (3, 3), (4, 3),
                (1, 2), (2, 2), (3, 2), (4, 2),
	                                    (4, 1),
		(0, 0), (1, 0), (2, 0), (3, 0),
	}

	print(len(solveA("input.txt")))
