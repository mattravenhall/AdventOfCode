#!/usr/bin/env python3

from functools import cache
import re

re_split = r"Card\s+(\d+):\s+([^|]*)\|(.*)"

total = 0
rewards = []
unprocessed = []


@cache
def _process(active: str, rewards: tuple) -> tuple[int, tuple]:
    return len(rewards[int(active)-1]), rewards[int(active)-1]


# Populate matches
for line in open("input.txt").readlines():
    card_id, winners, numbers = re.search(re_split, line).groups()
    winners = set(winners.split())
    numbers = set(numbers.split())

    # matches.append(len(winners & numbers))
    rewards.append(tuple(str(int(card_id) + i) for i in range(1, len(winners & numbers) + 1)))
    unprocessed.append(card_id)

rewards = tuple(rewards)

total += len(unprocessed)

# Process game
while unprocessed:
    active = unprocessed.pop(0)
    # print(f"Active card is {active}")
    # total += len(rewards[int(active)-1])
    # print(f"Total is now {total}")
    # unprocessed.extend(rewards[int(active)-1])
    # print(f"Unprocessed is now {unprocessed}")

    points, cards = _process(active, rewards)
    total += points
    unprocessed.extend(cards)

print(total)
