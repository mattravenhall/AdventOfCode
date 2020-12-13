#!/usr/bin/env python3

# Input format: operation (acc, jmp, or nop), argument (a signed number like +4 or -20).
# acc: alters the value of the accumulator
# jmp: jumps to a new instruction, e.g. jmp +1 would execute the next and jmp -1 the previous
# nop: does nothing

import sys

filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
commands = [command.strip().split() for command in open(filename).readlines()]

index = 0
visited = set()
accumulator = 0
inf_loop = False

while not inf_loop:
    visited.add(index)
    operation, argument = commands[index]

    # Update accumulator if required
    if operation == 'acc':
        accumulator += int(argument)

    # Identify next index
    if operation == 'jmp':
        index += int(argument)
    else:
        index += 1

    # Check we aren't about to re-visit an index
    if index in visited:
        inf_loop = True

print(accumulator)