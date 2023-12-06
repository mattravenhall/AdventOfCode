#!/usr/bin/env python3

time_distance = dict(zip(*[
    map(int, line.split()[1:])
    for line in open("input.txt").readlines()
]))

result = 1

for time_total, distance_to_beat in time_distance.items():
    ways_to_win = 0
    for time_hold in range(1, time_total+1):
        distance_travelled = time_hold * (time_total - time_hold)
        ways_to_win += distance_travelled > distance_to_beat
    result *= ways_to_win

print(result)
