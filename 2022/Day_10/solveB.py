#!/usr/bin/env python3

from collections import defaultdict
import re


def solveB(filename: str) -> str:

	X: int = 1
	store = defaultdict(int)

	commands = [line.strip().split() for line in open(filename).readlines()]
	commands = iter(commands)
	out_of_commands: bool = False

	drawing: str = ''

	in_addx: bool = False
	cycle = 0
	while not out_of_commands or cycle <= max(store.keys() if store.keys() else 0, 0):
		if cycle in store.keys():
			del store[cycle]

		cycle += 1

		# Process cycle command
		if not in_addx:
			command = next(commands, None)
			if command is None:
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

		# Draw to screen
		sprite = {X-1, X, X+1}
		position = (cycle-1) % 40
		drawing += '#' if position in sprite else '.'
		# print(f"[{cycle}] {drawing[-1]} pos={position} sprite={sorted(sprite)} X={X}")
		drawing = '\n'.join(re.findall('.{1,40}', drawing))

		# After cycle, update X
		X += store.get(cycle, 0)

	return drawing


if __name__ == '__main__':
	assert solveB("test.txt") == \
		"##..##..##..##..##..##..##..##..##..##..\n" \
		"###...###...###...###...###...###...###.\n" \
		"####....####....####....####....####....\n" \
		"#####.....#####.....#####.....#####.....\n" \
		"######......######......######......####\n" \
		"#######.......#######.......#######.....\n."

	print(solveB("input.txt"))
