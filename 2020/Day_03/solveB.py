#!/usr/bin/env python3

import numpy as np

map_matrix = np.genfromtxt('input.txt', dtype='str', comments=False, delimiter=1)


def count_trees(motion):
    MOTION = np.array(motion[::-1])  # down, right
    POS = np.array((0, 0))  # horizontal, vertical

    tree_count = 0
    while POS[0]+1 <= map_matrix.shape[0]:  # Continue until at the bottom
        if POS[1] + 1 >= map_matrix.shape[1]:
            POS[1] -= map_matrix.shape[1]

        map_matrix[POS[0]][POS[1]] = 'X' if map_matrix[POS[0]][POS[1]] in {'#', 'X'} else 'O'

        tree_count += 1 if map_matrix[POS[0]][POS[1]] in {'#', 'X'} else 0
        POS += MOTION

    # print('\n'.join(''.join(f"{x}" for x in y) for y in map_matrix))
    return tree_count

print(count_trees((1,1)) * count_trees((3,1)) * count_trees((5,1)) * count_trees((7,1)) * count_trees((1,2)))
