#!/usr/bin/env python3

from itertools import islice


PRIORITIES = f"-{''.join([chr(x) for x in range(97,123)])}{''.join([chr(x) for x in range(65,91)])}"


if __name__ == '__main__':
	count = 0
	with open("input.txt") as f:
		while True:
			group_rucksacks = list(islice(f, 3))
			if not group_rucksacks:
				break

			badge = list(set.intersection(*[set(rucksack.strip()) for rucksack in group_rucksacks]))
			assert len(badge) == 1
			badge = badge[0]

			priority = PRIORITIES.index(badge)

			count += priority
	print(count)
