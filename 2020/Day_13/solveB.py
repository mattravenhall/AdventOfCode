#!/usr/bin/env python

import math
import sys

filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
_, bus_ids_file = [line.strip() for line in open(filename)]


def solve_buses(bus_ids):
    bus_ids = {i: int(id) for i, id in enumerate(bus_ids.split(',')) if id != 'x'}
    bus_idx = sorted(bus_ids, key=bus_ids.get, reverse=True)

    timepoint = bus_ids[0]
    increment = 1

    while True:
        timepoint += increment

        for i, index in enumerate(bus_idx):
            id = bus_ids[index]
            remainder = (timepoint + index) % id
            if remainder != 0:
                break
            else:
                increment = math.prod([bus_ids[idx] for idx in bus_idx[:i+1]])
        else:
            return timepoint


assert solve_buses('17,x,13,19') == 3417
assert solve_buses('67,7,59,61') == 754018
assert solve_buses('67,x,7,59,61') == 779210
assert solve_buses('67,7,x,59,61') == 1261476
assert solve_buses('1789,37,47,1889') == 1202161486

print(solve_buses(bus_ids_file))
