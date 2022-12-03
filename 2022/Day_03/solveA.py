#!/usr/bin/env python3

PRIORITIES = f"-{''.join([chr(x) for x in range(97,123)])}{''.join([chr(x) for x in range(65,91)])}"


def parse_rucksack(items: str) -> int:
	comp_one, comp_two = items[:len(items)//2], items[len(items)//2:]
	shared_items = list(set(comp_one) & set(comp_two))

	assert len(shared_items) == 1
	priority = PRIORITIES.index(shared_items[0])

	return priority


print(sum([parse_rucksack(line.strip()) for line in open("input.txt").readlines()]))
