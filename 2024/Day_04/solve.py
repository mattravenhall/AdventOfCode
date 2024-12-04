#!/usr/bin/env python3

from typing import Optional


solution_a = 0
solution_b = 0

# Build grid
grid: list[str] = []
for line in open("./input.txt").readlines():
    grid.append(line.strip())


def not_in_range(grid: list, i: int, j: int):
    return i not in range(0, len(grid)) or j not in range(0, len(grid[0]))


def search_for_word(grid: list, x: int, y: int, word: str, direction: Optional[tuple[int]] = None, path: dict = {}) -> int:
    directions = [
        (-1, -1), (-1, 0), (-1, +1),
        ( 0, -1),          ( 0, +1),
        (+1, -1), (+1, 0), (+1, +1),
    ]
    if grid[x][y] == word[0]:
        path[word[0]] = (x, y)
        if len(word) < 2:
            return 1
        if direction is None:
            n_found = 0
            for direction in directions:
                i = x + direction[0]
                j = y + direction[1]
                if not_in_range(grid, i, j):
                    continue
                if search_for_word(grid, i, j, word[1:], direction, path):
                    n_found += 1
            return n_found
        else:
            i = x + direction[0]
            j = y + direction[1]
            if not_in_range(grid, i, j):
                return 0
            if search_for_word(grid, i, j, word[1:], direction, path):
                return 1
    else:
        return 0


def search_for_crossmas(grid: list, x: int, y: int):
    pairs = [
        ((x-1, y-1), (x+1, y+1)),
        ((x+1, y-1), (x-1, y+1)),
    ]
    for ((a_x, a_y), (b_x, b_y)) in pairs:
        # Out of bounds
        if {-1, len(grid)} & {a_x, a_y, b_x, b_y}:
            return False

        # Opposites are 'M' and 'S'
        if {grid[a_x][a_y], grid[b_x][b_y]} != {'M', 'S'}:
            return False

    return True


# Search grid
for x in range(len(grid)):
    for y in range(len(grid[0])):
        n_words_found = search_for_word(grid, x, y, "XMAS")
        solution_a += n_words_found

        if grid[x][y] == 'A':
            solution_b += search_for_crossmas(grid, x, y)

print(f"A: {solution_a}")
print(f"B: {solution_b}")
