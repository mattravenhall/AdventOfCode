#!/usr/bin/env python3

import copy
from typing import Literal


def shift_board(
        coords: dict[str, set[tuple[int]]],
        direction: Literal['N','S','W','E'],
        ) -> dict[str, set[tuple[int]]]:
    directions = {
        'N': lambda loc: (loc[0] + 1, loc[1]),
        'S': lambda loc: (loc[0] - 1, loc[1]),
        'W': lambda loc: (loc[0], loc[1] + 1),
        'E': lambda loc: (loc[0], loc[1] - 1),
    }
    new_coords = set()
    for i in range(board_limits[0]):
        for j in range(board_limits[1]):
            if (i, j) in coords['#'] | coords['O']:
                continue
            else:
                # Looking at a blank space, if a rock will move here - move it
                mover = directions[direction]((i, j))
                if mover in coords['O']:
                    coords['O'] -= {mover}
                    coords['O'].add((i, j))
    return coords


def print_board(coords, limits):
    for row in range(limits[0]):
        line = ''
        for col in range(limits[1]):
            if (row, col) in coords['O']:
                line += 'O'
            elif (row, col) in coords['#']:
                line += '#'
            else:
                line += '.'
        print(line)


# Collect initial rock locations
coords = {
    "#": set(),
    "O": set(),
}
for i, line in enumerate(open("input.txt").readlines()):
    line = line.strip()
    for j, c in enumerate(line):
        if c != '.':
            coords[c].add((i,j))
board_limits = (i+1, j+1)

previous = None
current = coords

# Shift north until stopped
while previous != current:
    previous = copy.deepcopy(current)
    current = shift_board(current, direction='N', limits=board_limits)

# Calculate score
print(sum([board_limits[0] - x[0] for x in current['O']]))
