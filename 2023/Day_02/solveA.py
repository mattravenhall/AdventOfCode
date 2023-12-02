#!/usr/bin/env python3

import re

re_game_id = r"^Game (\d+)"
re_count = r"(\d+) (blue|green|red)"

limits = {
	"red": 12,
	"green": 13,
	"blue": 14,
}

sum_ids = 0

for line in open("input.txt").readlines():
	for count, colour in re.findall(re_count, line):
		if int(count) > limits[colour]:
			break
	else:
		sum_ids += int(re.findall(re_game_id, line)[0])

print(sum_ids)
