#!/usr/bin/env python3

from collections import defaultdict
import re


RE_MOVE_COMMAND = r"^move (\d+) from (\d+) to (\d+)$"


if __name__ == '__main__':
	stacks_loaded = False
	stacks = defaultdict(list)

	run_type = "problem"
	input_file = {
		"problem": "input.txt",
		"test": "test.txt",
	}
	stack_labels = {
		"problem": " 1   2   3   4   5   6   7   8   9 ",
		"test": " 1   2   3 ",
	}
	top_crate = {
		"problem": 9,
		"test": 3,
	}

	for line in open(input_file[run_type]).readlines():
		line = line.rstrip('\n')
		# print(line)

		if line == stack_labels[run_type]:
			stacks_loaded = True
			# print(stacks)
			continue
		elif line == "":
			continue

		if not stacks_loaded:
			# Load initial stack states
			if line[1] != ' ':
				stacks[1].insert(0, line[1])
			if line[5] != ' ':
				stacks[2].insert(0, line[5])
			if line[9] != ' ':
				stacks[3].insert(0, line[9])
			if input_file[run_type] == "test.txt":
				continue
			if line[13] != ' ':
				stacks[4].insert(0, line[13])
			if line[17] != ' ':
				stacks[5].insert(0, line[17])
			if line[21] != ' ':
				stacks[6].insert(0, line[21])
			if line[25] != ' ':
				stacks[7].insert(0, line[25])
			if line[29] != ' ':
				stacks[8].insert(0, line[29])
			if line[33] != ' ':
				stacks[9].insert(0, line[33])
		else:
			# Enact move command
			amount, origin, destination = map(int, re.search(RE_MOVE_COMMAND, line).groups())

			# print(f"Moving {stacks[origin][-amount:]} to {destination}")
			stacks[destination].extend(stacks[origin][-amount:])
			del stacks[origin][-amount:]

	# Identify top crates
	print(''.join([stacks[i][-1] for i in range(1, top_crate[run_type]+1)]))
