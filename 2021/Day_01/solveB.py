#!/usr/bin/env python3

win_len = 3

measurements = list(map(lambda x: int(x.rstrip()), open('input.txt').readlines()))

print(sum([sum(measurements[i-win_len:i]) > sum(measurements[i-1-win_len:i-1]) for i in range(4,len(measurements)+1)]))
