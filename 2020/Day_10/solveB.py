#!/usr/bin/env python3

import sys


def num_combs(n):
    # Possible solution, unclear if n > 4
    assert 0 <= n <= 4, 'Function not generalised for given range'
    return (n*(n-1)/2) + 1


filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
joltages = sorted([int(line.strip()) for line in open(filename).readlines()])

device_joltage = max(joltages) + 3  # Could just add one to the 3 count later
joltages = [0] + joltages + [device_joltage]

path = [abs(joltages[i] - joltages[i+1]) for i in range(len(joltages)-1)]

total_combs = 1
gaps = 0
for digit in path:
    if digit == 1:
        gaps += 1
    elif digit == 3:
        total_combs *= num_combs(gaps)
        gaps = 0
    else:
        print(f"Unexpected gap length '{gaps}' encountered")

print(int(total_combs))
