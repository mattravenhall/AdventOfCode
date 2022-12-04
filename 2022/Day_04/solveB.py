#!/usr/bin/env python3

import re


RE_GROUPS = r"^(\d+)-(\d+),(\d+)-(\d+)$"


if __name__ == '__main__':
	overlaps = 0

	with open("input.txt") as f:
		for line in f.readlines():
			a_start, a_end, b_start, b_end = map(int, re.search(RE_GROUPS, line.strip()).groups())

			if set(range(a_start, a_end+1)) & set(range(b_start, b_end+1)):
				overlaps += 1

	print(overlaps)
