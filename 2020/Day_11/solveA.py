#!/usr/bin/env python3

import sys
import numpy as np

from collections import Counter

filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

read_matrix = np.genfromtxt(filename, dtype='str', comments=None, delimiter=1, deletechars='')
matrix_height, matrix_width = read_matrix.shape
write_matrix = None


def get_neighbours(matrix, i, j):
    matrix_h, matrix_w = matrix.shape
    neighbours = []
    if i > 0:
        if j > 0:
            neighbours.append(matrix[i-1][j-1])  # UL
        neighbours.append(matrix[i-1][j])  # UM
        if j < matrix_w-1:
            neighbours.append(matrix[i-1][j+1])  # UR
    if j > 0:
        neighbours.append(matrix[i][j-1])  # LM
    if j < matrix_w-1:
        neighbours.append(matrix[i][j+1])  # RM
    if i < matrix_h-1:
        if j > 0:
            neighbours.append(matrix[i+1][j-1])  # BL
        neighbours.append(matrix[i+1][j])  # BM
        if j < matrix_w-1:
            neighbours.append(matrix[i+1][j+1])  # BR
    #
    # neighbours = [UL, UM, UR,
    #               LM,     RM,
    #               BL, BM, BR]

    return neighbours


while not np.array_equal(read_matrix, write_matrix) or write_matrix is None:
    if write_matrix is not None:
        read_matrix = write_matrix.copy()
    else:
        write_matrix = read_matrix.copy()
    for i in range(matrix_height):
        for j in range(matrix_width):
            neighbours = get_neighbours(read_matrix, i, j)
            neighbour_counts = Counter(neighbours)
            if read_matrix[i][j] == 'L' and neighbour_counts['#'] == 0:
                write_matrix[i][j] = '#'
            elif read_matrix[i][j] == '#' and neighbour_counts['#'] >= 4:
                write_matrix[i][j] = 'L'

final_counts = Counter(read_matrix.flatten())
print(final_counts['#'])
