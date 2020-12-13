#!/usr/bin/env python3

import sys
from collections import Counter

filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
joltages = sorted([int(line.strip()) for line in open(filename).readlines()])

device_joltage = max(joltages) + 3  # Could just add one to the 3 count later
joltages = [0] + joltages + [device_joltage]

counts = Counter([abs(joltages[i] - joltages[i+1]) for i in range(len(joltages)-1)])
print(counts[1] * counts[3])
