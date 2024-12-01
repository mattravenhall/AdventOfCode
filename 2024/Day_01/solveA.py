#!/usr/bin/env python3

import re

# Part A
values_left, values_right = [], []
for line in open("./input.txt").readlines():
	value_left, value_right = map(int, re.findall(r'\d+', line))
	values_left.append(value_left)
	values_right.append(value_right)


values_left = sorted(values_left)
values_right = sorted(values_right)

total = 0
for pair in range(len(values_left)):
	total += abs(values_left.pop(0) - values_right.pop(0))

print(total)
