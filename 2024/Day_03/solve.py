#!/usr/bin/env python3.10

import math
import re

re_muls_A = r"mul\((\d+),(\d+)\)"
re_muls_B = r"((mul\((\d+),(\d+)\))|(do\(\))|(don't\(\)))"

solutions = {
	"A": 0,
	"B": 0,
}

active = True
for line in open("./input.txt").readlines():
	solutions["A"] += sum([math.prod(map(int, pair)) for pair in re.findall(re_muls_A, line)])

	mul_w_cmds = re.finditer(re_muls_B, line)
	for sequence in mul_w_cmds:
		match sequence.group():
			case string if string.startswith('mul'):
				if active:
					solutions["B"] += math.prod(map(int, sequence.groups()[2:4]))
			case "do()":
				active = True
			case "don't()":
				active = False
			case _:
				pass

print(f"A: {solutions['A']}")
print(f"B: {solutions['B']}")
