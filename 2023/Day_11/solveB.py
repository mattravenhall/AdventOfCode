#!/usr/bin/env python3

from itertools import combinations

space = []
galaxies = set()
n_cols = None
expansions = {
    "rows": set(),
    "cols": set(),
}
for i, line in enumerate(open("input.txt").readlines()):
    line = line.strip()
    if n_cols is None:
        n_cols = len(line)
        expansions["cols"] = {i for i in range(n_cols)}

    line = line.strip()
    space.append(line)
    if '#' not in line:
        space.append(line)
        expansions["rows"].add(i)
    else:
        for j, tile in enumerate(line):
            if tile == '#':
                galaxies.add((i, j))
                expansions["cols"] -= {j}

# Get manhattan distance between all pairs
total = 0
for (g1x, g1y), (g2x, g2y) in combinations(galaxies, 2):
    n_x_row = len(expansions["rows"] & set(range(min(g1x, g2x), max(g1x, g2x))))
    n_x_col = len(expansions["cols"] & set(range(min(g1y, g2y), max(g1y, g2y))))
    n_expansions = n_x_row + n_x_col
    total += (abs(g1x - g2x) + abs(g1y - g2y)) + (n_expansions * 999999)  # manhattan_distance + (n. expansions - 1)

print(total)
