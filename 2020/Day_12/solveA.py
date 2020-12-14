#!/usr/bin/env python

import sys
import numpy as np

from collections import deque

filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
orders = [line.strip() for line in open(filename).readlines()]


dir_to_vector = {
    'N': np.array((0, 1)),
    'E': np.array((1, 0)),
    'S': np.array((0, -1)),
    'W': np.array((-1, 0))
}

compass = deque('ENWS')

start = (0, 0)
forward = dir_to_vector[compass[0]]
distance = start

for order in orders:
    magnitude = int(order[1:])

    if order[0] in 'LR':
        # Update compass with rotation
        magnitude = -1 * magnitude if order[0] == 'L' else magnitude
        compass.rotate(magnitude//90)
        continue
    elif order[0] == 'F':
        # Forward is always the first index of our compass
        vector = dir_to_vector[compass[0]]
    elif order[0] in 'NESW':
        vector = dir_to_vector[order[0]]

    distance += (vector * magnitude)

manhattan_distance = abs(distance)[0] + abs(distance)[1]
print(manhattan_distance)
