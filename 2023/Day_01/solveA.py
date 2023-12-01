#!/usr/bin/env python3

total = 0

for line in open("input.txt").readlines():
	first = None
	last = None
	for c in line:
		if c.isdigit():
			if first is None:
				first = c
			else:
				last = c
	print(f"{first=} - {last=}")
	if last is None:
		last = first
	if first is not None:
		total += int(first + last)

print(total)
