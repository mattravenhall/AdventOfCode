#!/usr/bin/env python3

from collections import deque
from copy import deepcopy

solution_a = 0
solution_b = 0

start = (-1, -1)
obstacle_candidates = set()

def out_of_range(grid, x, y) -> bool:
    if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]):
        return True
    else:
        return False

# Build grid
grid: list[list[str]] = []
for i, line in enumerate(open("./input.txt").readlines()):
    if line == "":
        breakpoint()
    line = line.strip()
    grid.append(list(line))

    # Collect start position
    for j, value in enumerate(line):
        if value == '^':
            start = (i, j)


def walk_guard(grid: list[str], part_a=False, debug = None) -> int:
    directions = deque([(-1, 0), (0, 1), (1, 0), (0, -1)])
    start_direction = directions[0]
    visited = set()
    position = start
    while True:

        # Scout next position
        next_x, next_y = tuple(map(sum, zip(position, directions[0])))

        # If going out of range, exit
        if out_of_range(grid, next_x, next_y):
            visited.add(position)
            return visited

        # Check for obstacles
        while grid[next_x][next_y] in {'#', 'O'}:
            # Change direct when heading into a '#'
            if debug is not None:
                debug[position[0]][position[1]] = '+'
            directions.rotate(-1)
            next_x, next_y = tuple(map(sum, zip(position, directions[0])))
        
        if grid[next_x][next_y] == '.':
            # If the next space is empty, it's an obstacle candidate for Part B
            if part_a:
                if (next_x, next_y) != start:
                    obstacle_candidates.add((next_x, next_y))
            
            # Update debug grid
            if debug is not None:
                if directions[0][0] == 0:
                    debug[position[0]][position[1]] = '-'
                elif directions[0][1] == 0:
                    debug[position[0]][position[1]] = '|'

        if part_a:
            # [Part A] Check if we're about to return to start
            visited.add(position)
            if (next_x, next_y) == start and directions[0] == start_direction:
                return visited
        else:
            # [Part B] Check if we're in a loop (about to repeat a step)
            if (position, directions[0]) in visited:
                if debug is not None:
                    print('\n'+'\n'.join([''.join(line) for line in debug]))
                return -1
            visited.add((position, directions[0]))

        # Update position to next step
        position = tuple(map(sum, zip(position, directions[0])))

# Part A
a_visited = walk_guard(grid, part_a=True)
solution_a = len(a_visited)

# Part B
print(f"Considering {len(a_visited)} candidates")
for i, (obs_x, obs_y) in enumerate(a_visited):
    if (obs_x, obs_y) == start:
        continue

    # Add obstacle at the candidate location, check for loops
    new_grid = deepcopy(grid)
    new_grid[obs_x][obs_y] = 'O'
    debug_grid = deepcopy(new_grid)
    solution_b += (walk_guard(new_grid) == -1)

print(f"A: {solution_a}")
print(f"B: {solution_b}")
