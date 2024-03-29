#!/usr/bin/env python3

from operator import add

# HashMap of valid directions and their valid connectors
directions = {
    (-1,  0): {'|', 'F', '7'},  # Up
    ( 0, -1): {'-', 'F', 'L'},  # Left
    ( 0,  1): {'-', '7', 'J'},  # Right
    ( 1,  0): {'|', 'L', 'J'},  # Down
}
valid_directions = {
    'S': {(-1, 0), (0, -1), (0, 1), (1, 0)},
    '|': {(-1, 0), (1, 0)},
    '-': {(0, -1), (0, 1)},
    'F': {(0, 1), (1, 0)},
    '7': {(0, -1), (1, 0)},
    'L': {(-1, 0), (0, 1)},
    'J': {(-1, 0), (0, -1)},
}


# Allow each addition of vectors
def _vec_add(vec_a: tuple[int], vec_b: tuple[int]) -> tuple[int]:
    return tuple(map(add, vec_a, vec_b))


# Find valid connecting pipes for a given start point
def _find_next_pipes(start: tuple[int], seen: set[tuple[int]] = set()) -> tuple[tuple[int]]:
    results = []
    srow, scol = start
    for direction in valid_directions[schematic[srow][scol]]:
        connectors = directions[direction]
        candidate = _vec_add(start, direction)

        # Ignore out of bounds
        if not (0 <= candidate[0] < len(schematic)) or not (0 <= candidate[1] < len(schematic[0])):
            continue

        # Ignore previously seen locations, if any
        if candidate in seen:
            continue

        # If a valid connector exists, add location to results        
        if schematic[candidate[0]][candidate[1]] in connectors:
            results.append(candidate)
    
    return results


# Update scout location and path
def _update_scout(location: tuple[int], path: set[tuple[int]]) -> tuple[tuple[int], set[tuple[int]]]:
    path.append(location)
    location = _find_next_pipes(location, seen=path)[0]
    return location, path


# Parse input into a matrix
schematic: list[str] = []
for i, line in enumerate(open("input.txt").readlines()):
    line = line.strip()
    schematic.append(line)
    if 'S' in line:
        start: tuple[int] = (i, line.index('S'))

# Find starting positions for scouts    
scout_a, scout_b = _find_next_pipes(start)
path_scout_a = [start]
path_scout_b = [start]

# Start searching
while scout_a != scout_b:
    # Move each scout to its next position
    scout_a, path_scout_a = _update_scout(scout_a, path_scout_a)
    scout_b, path_scout_b = _update_scout(scout_b, path_scout_b)

print(len(path_scout_a))
