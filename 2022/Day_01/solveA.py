#!/usr/bin/env python3

from collections import defaultdict

elf_calories = defaultdict(int)

elf_id = 1
for line in open('input.txt').readlines():
	line = line.strip()
	if line == '':
		elf_id += 1
	else:
		elf_calories[elf_id] += int(line)

most_calories = max(elf_calories.values())

print(most_calories)
