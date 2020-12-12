#!/usr/bin/env python3

with open('input.txt') as f:
    group_count = 0
    group_values = None
    for line in f.readlines():
        line = line.strip()
        if line == '':
            # Group end
            group_count += len(group_values)
            group_values = None
            continue
        elif group_values is None:
            # Group start
            group_values = set(line)
        else:
            # Group middle
            group_values = group_values.intersection(set(line))

group_count += len(group_values)
print(group_count)
