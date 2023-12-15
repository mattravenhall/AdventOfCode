#!/usr/bin/env python3

import copy
from typing import Literal


def shift_board(
        coords: dict[str, set[tuple[int]]],
        direction: Literal['N','S','W','E'],
        limits: tuple[int]
    ) -> dict[str, set[tuple[int]]]:
    def _in_bounds(location: tuple[int], limits: tuple[int]) -> bool:
        return (0 <= location[0] < limits[0]) and (0 <= location[1] < limits[1])

    directions = {
        'S': lambda loc: (loc[0] + 1, loc[1]),
        'N': lambda loc: (loc[0] - 1, loc[1]),
        'E': lambda loc: (loc[0], loc[1] + 1),
        'W': lambda loc: (loc[0], loc[1] - 1),
    }

    row_iter = range(limits[0])[::-1] if direction == 'S' else range(limits[0])
    col_iter = range(limits[1])[::-1] if direction == 'E' else range(limits[1])

    n_to_move = len(coords['O'])
    for i in row_iter:
        for j in col_iter:
            if (i, j) in coords['O']:
                new_loc = (i, j)
                scout = directions[direction](new_loc)
                while scout not in coords['#'] | coords['O'] and _in_bounds(scout, limits=board_limits):
                    new_loc = scout
                    scout = directions[direction](scout)
                if (i, j) != new_loc:
                    coords['O'] -= {(i, j)}
                    coords['O'].add(new_loc)
                n_to_move -= 1
                if n_to_move == 0:
                    break
    
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

def _board_to_key(board):
    return tuple(map(tuple, map(sorted, board.values())))

# Rotate north, west, south, east for 1000000000 cycles
grids = {}
total_cycles = 1000000000
print('--- i = 0')
for i in range(total_cycles):
    for direction in "NWSE":
        current = shift_board(current, direction=direction, limits=board_limits)
        board_key = _board_to_key(current)
    # print_board(current, limits=board_limits)
    # print(f"--- i = {i+1}")

    if board_key in grids:
        previously_seen = grids[board_key]
        len_repeat = i - previously_seen
        # print(f"Repetition observed with {previously_seen}")
        break
    else:
        grids[board_key] = i

# Determine cycles required for final state and rotate to it
for _ in range((total_cycles - (i+1)) % len_repeat):
    for direction in "NWSE":
        current = shift_board(current, direction=direction, limits=board_limits)

print(sum([board_limits[0] - x[0] for x in current['O']]))
