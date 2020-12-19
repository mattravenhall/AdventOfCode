#!/usr/bin/env python

import sys
import re
from itertools import product

filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

mask = None
memory = dict()
mask_regex = r'mask = (\w)*'
mem_regex = r'mem\[(\d*)\] = (\d*)'


def mask_value(mask, value):
    value = f"{int(value):b}".zfill(36)
    result = ''.join([
        v if mask[i] in 'X0' else mask[i]
        for i, v in enumerate(value)
    ])
    return result


for line in open(filename):
    if line.strip() == '':
        break

    instruction, value = [x.strip() for x in line.strip().split('=')]

    if instruction == 'mask':
        # Update mask
        mask = value
    elif instruction.startswith('mem'):
        # Mask locations
        location = int(re.sub('\D', '', instruction))
        base_loc = list(mask_value(mask, location))

        X_indexes = [int(i) for i, c in enumerate(mask) if c == 'X']
        X_replacements = [''.join(x) for x in product('01', repeat=len(X_indexes))]

        locations = set()
        for X_replacement in X_replacements:
            new_location = base_loc
            for index, char in zip(X_indexes, X_replacement):
                new_location[index] = char
            locations.add(''.join(new_location))

        for location in locations:
            # print(f"Location: {location} ({int('0b'+location,2)}) --> {value}")
            memory[location] = int(value)

print(sum(memory.values()))
