#!/usr/bin/env python

import sys

filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
timepoint, bus_ids = [line.strip() for line in open(filename)]

start_time = int(timepoint)
timepoint = start_time
bus_ids = [int(id) for id in bus_ids.split(',') if id != 'x']


next_bus_id = []
while not next_bus_id:
    timepoint += 1
    next_bus_id = [id for id in bus_ids if timepoint % id == 0][0]

answer = (timepoint - start_time) * next_bus_id
print(answer)

