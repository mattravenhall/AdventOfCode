#!/usr/bin/env python3

import numpy as np

MOTION = np.array((1, 3))  # down, right
POS = np.array((0, 0))  # horizontal, vertical

map_matrix = np.genfromtxt('input.txt', dtype='str', comments=False, delimiter=1)

tree_count = 0
while POS[0]+1 <= map_matrix.shape[0]:  # Continue until at the bottom
    if POS[1] + 1 >= map_matrix.shape[1]:
        POS[1] -= map_matrix.shape[1]

    map_matrix[POS[0]][POS[1]] = 'X' if map_matrix[POS[0]][POS[1]] in {'#', 'X'} else 'O'

    tree_count += 1 if map_matrix[POS[0]][POS[1]] in {'#', 'X'} else 0
    print(f"Tree Count: {tree_count}")
    POS += MOTION

# print('\n'.join(''.join(f"{x}" for x in y) for y in map_matrix))
print(tree_count)
