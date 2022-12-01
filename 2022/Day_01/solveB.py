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

top_x_calories = 0
for _ in range(3):
	top_elf = max(elf_calories, key=elf_calories.get)
	top_x_calories += elf_calories[top_elf]
	elf_calories.pop(top_elf)

print(top_x_calories)
