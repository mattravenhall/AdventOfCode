#!/usr/bin/env python3

with open('input.txt') as f:
    group_count = 0
    group_values = set()
    for line in f.readlines():
        line = line.strip()
        if line == '':
            group_count += len(group_values)
            group_values = set()
            continue
        group_values.update(set(line))

group_count += len(group_values)
print(group_count)
