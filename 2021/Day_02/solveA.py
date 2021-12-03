#!/usr/bin/env python3

from collections import defaultdict


tallies = defaultdict(int)

for line in open('input.txt').readlines():
	command, magnitude = line.rstrip().split()
	tallies[command] += int(magnitude)


print(tallies["forward"] * (tallies["down"] - tallies["up"]))
