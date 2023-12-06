#!/usr/bin/env python3

time_total, distance_to_beat = [
    int(''.join(line.split()[1:]))
    for line in open("input.txt").readlines()
]

ways_to_win = 0
for time_hold in range(1, time_total+1):
    distance_travelled = time_hold * (time_total - time_hold)
    ways_to_win += distance_travelled > distance_to_beat

print(ways_to_win)
