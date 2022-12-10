#!/usr/bin/env python3

from collections import defaultdict


def solveA(filename: str) -> int:

	X: int = 1
	store = defaultdict(int)
	reports: list[int] = []

	commands = [line.strip().split() for line in open(filename).readlines()]
	n_commands = len(commands)
	commands = iter(commands)
	out_of_commands: bool = False

	in_addx: bool = False
	cycle = 0
	while not out_of_commands or cycle <=  max(store.keys() if store.keys() else 0, 0):
		if cycle in store.keys():
			del store[cycle]

		cycle += 1

		# Process cycle command
		if not in_addx:
			command = next(commands, None)
			if command == None:
				out_of_commands = True
		else:
			in_addx = False
			command = '-'

		match command:
			case ["noop"]:
				pass
			case ["addx", value]:
				store[cycle+1] += int(value)
				in_addx = True
			case _:
				pass

		# Report signal strength on specific cycles
		if (cycle - 20) % 40 == 0:
			reports.append(cycle * X)

		# After cycle, update X
		X += store.get(cycle, 0)

	return sum(reports)


if __name__ == '__main__':
	assert solveA("test.txt") == 13140

	print(solveA("input.txt"))
