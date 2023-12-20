#!/usr/bin/env python3

"""
Find the shortest path from top-left to bottom-right.
Paths cannot include more than three moves in a single direction.
Visited nodes cannot be revisited.
"""

import math
from operator import add
import heapq


def _vec_add(vec_a: tuple[int], vec_b: tuple[int]) -> tuple[int]:
    """Allow each addition of vectors"""
    return tuple(map(add, vec_a, vec_b))


def _in_bounds(location: tuple[int], limits: tuple[int]) -> bool:
    """Check whether a position vector is within the given bound"""
    return (0 <= location[0] < limits[0]) and (0 <= location[1] < limits[1])


def shortest_path(grid: list[str], start: tuple[int], end: tuple[int]) -> int:
    unvisited = [(0, start, None, 0, '')]  # Heat loss, coords, in direction, n. repeats, path
    visited = set()

    while unvisited:
        # Set current node to the unvisited node with the lowest total heat loss
        heat_loss, current_node, in_direction, n_repeats, path = heapq.heappop(unvisited)

        # Break if we've reached the destination
        if current_node == end:
            path = set(map(eval, path.split('|')[1:]))
            for i, row in enumerate(grid):
                line = ''
                for j, col in enumerate(row):
                    if (i, j) in path:
                        line += 'x'
                    else:
                        line += str(col)
                print(line)
            return heat_loss
        
        # Skip visited nodes
        if (current_node, in_direction, n_repeats) in visited:
            continue

        # Mark node as visited
        visited.add((current_node, in_direction, n_repeats))

        # Consider nodes adjacent to current node
        for direction in {(0, 1), (0, -1), (1, 0), (-1, 0)}:
            child_node = _vec_add(current_node, direction)
            # print(f"{current_node=} {child_node=} {direction=}")

            # Ignore out-of-bounds nodes
            if not _in_bounds(child_node, limits=(len(grid), len(grid[0]))):
                continue

            # Ignore reverse movement
            if tuple(i * -1 for i in direction) == in_direction:
                continue

            # Do not turn until going straight four times
            if n_repeats < 4 and (direction != in_direction) and (in_direction is not None):
                continue

            # Update number of repeat directions, skip if it would go over 10
            if direction == in_direction:
                # Avoid moving in the same direction more than 10 times
                if n_repeats >= 10:
                    continue
                else:
                    current_repeats = n_repeats + 1
            else:
                current_repeats = 1

            # Calculate heat_loss for child node
            current_heat_loss = heat_loss + int(grid[child_node[0]][child_node[1]])

            # Add valid child nodes to unvisited, if not visited
            # if (child_node, direction, current_repeats) not in visited:
            heapq.heappush(unvisited, (current_heat_loss, child_node, direction, current_repeats, f"{path}|{child_node}"))


# Load grid into memory
grid: list[str] = []
for line in open("input.txt").readlines():
    grid.append([int(i) for i in line.strip()])

part_one = shortest_path(grid, start=(0, 0), end=(len(grid)-1, len(grid[0])-1))

print(part_one)
