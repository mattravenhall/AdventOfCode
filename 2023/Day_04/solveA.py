#!/usr/bin/env python3

import re

re_split = r"Card\s+(\d+):\s+([^|]*)\|(.*)"

total = 0

for line in open("input.txt").readlines():
    card_id, winners, numbers = re.search(re_split, line).groups()
    winners = set(winners.split())
    numbers = set(numbers.split())

    matches = winners & numbers
    if matches:
        points = 2 ** (len(matches) - 1)
        # print(f"Card {card_id}: {points} points")
        total += points

print(total)
