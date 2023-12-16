#!/usr/bin/env python3

from operator import add


def _vec_add(vec_a: tuple[int], vec_b: tuple[int]) -> tuple[int]:
    """Allow each addition of vectors"""
    return tuple(map(add, vec_a, vec_b))


def _in_bounds(location: tuple[int], limits: tuple[int]) -> bool:
    """Check whether a position vector is within the given bound"""
    return (0 <= location[0] < limits[0]) and (0 <= location[1] < limits[1])


def count_energised(photons: set[tuple[tuple[int]]], grid: list[list[str]]) -> int:
    """Iterate photon paths and return the total number of tiles energised"""
    # Store photons in a hashset: {(location, direction), ...}

    # Whilst photons are travelling
    observed = set()
    while photons:
        for _ in range(len(photons)):
            position, direction = photons.pop()

            # Add old location and direction to observed
            observed.add((position, direction))
            new_photons = set()

            # Update position and direction as required
            # If location in \/, potentially change direction vector
            # If location in -|, potentially replace photon with two photons
            if grid[position[0]][position[1]] == "\\":
                new_direction = (direction[1], direction[0])
                new_photons.add((_vec_add(position, new_direction), new_direction))
            elif grid[position[0]][position[1]] == "/":
                new_direction = (-direction[1], -direction[0])
                new_photons.add((_vec_add(position, new_direction), new_direction))
            elif (
                grid[position[0]][position[1]] == "-" and direction[0] != 0
            ):  # Moving vertically
                for new_direction in [(0, 1), (0, -1)]:
                    new_photons.add((_vec_add(position, new_direction), new_direction))
            elif (
                grid[position[0]][position[1]] == "|" and direction[1] != 0
            ):  # Moving horizontally
                for new_direction in [(1, 0), (-1, 0)]:
                    new_photons.add((_vec_add(position, new_direction), new_direction))
            else:
                # Unimpeded travel
                new_photons.add((_vec_add(position, direction), direction))

            # Add next location and direction to photons, if unobserved and in bounds
            for new_position, new_direction in new_photons:
                if (new_position, new_direction) not in observed and _in_bounds(
                    new_position, limits
                ):
                    photons.add((new_position, new_direction))

    # Count number of energised positions
    return len({x[0] for x in observed})


# Read grid into memory
grid = []
for line in open("input.txt").readlines():
    grid.append(list(line.strip()))
limits = (len(grid), len(grid[0]))

# Find number of energised titles when starting in the top left
score_part_1 = count_energised(photons={((0, 0), (0, 1))}, grid=grid)

# Find maximum number of energised titles when starting at any border edge
score_part_2 = 0
origin_top = [{((0, i), (1, 0))} for i in range(len(grid[0]))]
origin_bottom = [{((len(grid) - 1, i), (-1, 0))} for i in range(len(grid[0]))]
origin_left = [{((i, 0), (0, 1))} for i in range(len(grid))]
origin_right = [{((i, len(grid[0]) - 1), (0, -1))} for i in range(len(grid))]

for photons in origin_top + origin_bottom + origin_left + origin_right:
    # print(f"Origin: {photons}", end='')
    n_energised = count_energised(photons=photons, grid=grid)
    if n_energised > score_part_2:
        score_part_2 = n_energised
    # print(f" energised {n_energised} tiles")

# Print scores
print(f"Part 1: {score_part_1}")
print(f"Part 2: {score_part_2}")
