#!/usr/bin/env python3

aim, horizontal, depth = 0, 0, 0

for line in open('input.txt').readlines():
	command, magnitude = line.rstrip().split()
	magnitude = int(magnitude)

	if command == 'forward':
		horizontal += magnitude
		depth += aim * magnitude
	else:
		aim += magnitude if command == 'down' else -magnitude

print(horizontal * depth)
