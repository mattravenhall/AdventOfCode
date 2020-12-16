#!/usr/bin/env python

import sys
import math
import numpy as np

from collections import deque

filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
orders = [line.strip() for line in open(filename).readlines()]


dir_to_vector = {
    'N': np.array((1., 0.)),
    'E': np.array((0., 1.)),
    'S': np.array((-1., 0.)),
    'W': np.array((0., -1.))
}

compass = deque('ENWS')

ship = np.array((0., 0.))
waypoint = np.array((1., 10.))
forward = waypoint


def rotate(angle, waypoint, origin=(0, 0)):
    # Thanks Google
    angle = math.radians(angle)

    ox, oy = origin
    px, py = waypoint

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

    return np.array((qx, qy))
    # return np.array((int(round(qx)), int(round(qy))))


for order in orders:
    magnitude = int(order[1:])
    # print(f"[{order}]")

    if order[0] in 'LR':
        magnitude = -1 * magnitude if order[0] == 'L' else magnitude
        # print(f"Rotating {order[0]} {magnitude} from {waypoint}")
        waypoint = rotate(magnitude, waypoint)
        # print(f"Waypoint now at {waypoint}")
    elif order[0] == 'F':
        # Forwards is towards the waypoint
        # print(f"Moving ship from {ship} towards {waypoint}, at speed {magnitude}")
        ship += (waypoint * magnitude)
        # print(f"Ship now at {ship}")
    elif order[0] in 'NESW':
        # Compass directions moves the waypoint
        # print(f"Moving waypoint {waypoint} {order[0]} at speed {magnitude}")
        waypoint += dir_to_vector[order[0]] * magnitude
        # print(f"Waypoint is now at {waypoint}")

manhattan_distance = abs(ship)[0] + abs(ship)[1]
print(round(manhattan_distance))
