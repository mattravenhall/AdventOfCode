#!/usr/bin/env python3

import re


RE_GROUPS = r"^(\d+)-(\d+),(\d+)-(\d+)$"


if __name__ == '__main__':
	fully_contained = 0

	with open("input.txt") as f:
		for line in f.readlines():
			a_start, a_end, b_start, b_end = map(int, re.search(RE_GROUPS, line.strip()).groups())

			if ((a_start >= b_start) and (a_end <= b_end)) or ((b_start >= a_start) and (b_end <= a_end)):
				fully_contained += 1

	print(fully_contained)
