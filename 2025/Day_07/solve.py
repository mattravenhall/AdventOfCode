#!/usr/bin/env python3

from collections import defaultdict


def solve(path: str) -> int:
    start = None
    beams = defaultdict(int)
    n_splits = 0
    lines = map(
        lambda x: x.strip(),
        open(path).readlines()
    )

    for y, line in enumerate(lines): 
        if set(line) == {'.'}:
            # Ignore empty rows
            continue
        elif start is None:
            # Identify start location
            start = line.index('S')
            beams[start] += 1
        else:
            # Interact with splitters
            new_beams = defaultdict(int)
            for beam in beams:
                if line[beam] == '^':
                    new_beams[beam-1] += beams[beam]
                    new_beams[beam+1] += beams[beam]
                    n_splits += 1 
                else:
                    new_beams[beam] += beams[beam]
            beams = new_beams
    
    n_timelines = sum(beams.values())

    return n_splits, n_timelines


assert solve("test.txt") == (21, 40)

print(solve("input.txt"))

