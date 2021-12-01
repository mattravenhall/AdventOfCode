#!/usr/bin/env python3

measurements = list(map(lambda x: int(x.rstrip()), open('input.txt').readlines()))

print(sum([measurements > measurements[i-1] for i, x in enumerate(measurements) if i > 0]))
