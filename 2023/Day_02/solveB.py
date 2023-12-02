#!/usr/bin/env python3

import re
from math import prod

re_game_id = r"^Game (\d+)"
re_count = r"(\d+) (blue|green|red)"

sum_powers = 0

for line in open("input.txt").readlines():

	counts = {
		"red": 0,
		"green": 0,
		"blue": 0,
	}

	for count, colour in re.findall(re_count, line):
		count = int(count)
		if count > counts[colour]:
			counts[colour] = count

	sum_powers += prod(counts.values())

print(sum_powers)
