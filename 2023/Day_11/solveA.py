#!/usr/bin/env python3

from itertools import combinations

space = []
for line in open("input.txt").readlines():
    line = line.strip()
    space.append(line)
    if '#' not in line:
        space.append(line)

# Transpose and expand columns
space = list(map(list, zip(*space)))
expanded = []
for line in space:
    # line = line.strip()
    expanded.append(line)
    if '#' not in line:
        expanded.append(line)
space = list(map(list, zip(*expanded)))

# Find galaxies
galaxies = set()
for i, line in enumerate(space):
    for j, tile in enumerate(line):
        if tile == '#':
            galaxies.add((i, j))

# Get manhattan distance between all pairs
total = 0
for (g1x, g1y), (g2x, g2y) in combinations(galaxies, 2):
    total += abs(g1x - g2x) + abs(g1y - g2y)  # manhattan_distance

print(total)
