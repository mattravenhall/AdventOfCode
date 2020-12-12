#!/usr/bin/env python3

seat_ids = set()

with open('input.txt') as f:
    for line in f.readlines():
        rows = [row for row in range(127+1)]
        cols = [col for col in range(7+1)]
        code = line.strip()

        for direction in code:
            if direction == 'F':
                rows = rows[:round(len(rows)/2)]
            elif direction == 'B':
                rows = rows[round(len(rows)/2):]
            elif direction == 'L':
                cols = cols[:round(len(cols)/2)]
            elif direction == 'R':
                cols = cols[round(len(cols)/2):]
        row = rows[0]
        col = cols[0]
        seat_ids.add((row*8) + col)

seat_ids = sorted(seat_ids)
for i, id in enumerate(seat_ids):
    if i in [0, len(seat_ids)]:
        continue
    if not (id-1 == seat_ids[i-1]):
        print(id-1)
