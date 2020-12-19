#!/usr/bin/env python

import sys
import re

filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

mask = None
memory = dict()
mask_regex = r'mask = (\w)*'
mem_regex = r'mem\[(\d*)\] = (\d*)'

for line in open(filename):
    if line.strip() == '':
        break
    instruction, value = [x.strip() for x in line.strip().split('=')]

    if instruction == 'mask':
        mask = value
    elif instruction.startswith('mem'):
        location = int(re.sub('\D', '', instruction))
        value = f"{int(value):b}".zfill(36)

        result = ''.join([
            v if mask[i] == 'X' else mask[i]
            for i, v in enumerate(value)
        ])

        memory[location] = int('0b'+result, 2)

        # print(f"--------"+'-'*36)
        # print(f"Value : {value}")
        # print(f"Mask  : {mask}")
        # print(f"Result: {result}")
        # print(f"memory[{location}] = {int('0b'+result, 2)}")

print(sum(memory.values()))
