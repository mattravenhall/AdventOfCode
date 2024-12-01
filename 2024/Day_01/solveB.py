#!/usr/bin/env python3

from collections import defaultdict
import re

# Part B
values_left, values_right = [], defaultdict(int)
for line in open("./input.txt").readlines():
	value_left, value_right = map(int, re.findall(r'\d+', line))
	values_left.append(value_left)
	values_right[value_right] += 1

total = 0
for value in values_left:
	total += value * values_right[value]

print(total)
