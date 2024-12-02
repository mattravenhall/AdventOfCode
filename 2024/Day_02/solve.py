#!/usr/bin/env python3

safe_reports = {
	"A": 0,
	"B": 0,
}


def line_is_safe(levels: list[int]) -> bool:
	direction = None
	for left, right in zip(levels, levels[1:]):
		direction_check = left > right
		if direction is None:
			direction = left > right
		else:
			if direction != direction_check:
				return False

		if abs(left - right) not in {1, 2, 3}:
			return False
	else:
		return True


for line in open("./input.txt").readlines():
	levels = list(map(int, line.split(' ')))

	if line_is_safe(levels):
		safe_reports["A"] += 1
		safe_reports["B"] += 1
	else:
		# Check if dropping a value will make the line safe
		for i in range(len(levels)):
			levels_wo_i = levels[:i] + levels[i+1:]
			if line_is_safe(levels_wo_i):
				safe_reports["B"] += 1
				break


print(f"A: {safe_reports['A']}")
print(f"B: {safe_reports['B']}")
