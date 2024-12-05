#!/usr/bin/env python3

from collections import defaultdict

solution_a: int = 0
solution_b: int = 0

global rules
global rules_inv

rules = defaultdict(set)  # Should this be a graph?
rules_inv = defaultdict(set)


def get_middle(update: list) -> int:
    return int(update[int((len(update) - 1)/2)])


def quicksort(array: list):
    if len(array) <= 1:
        return array
    
    pivot = array[len(array) // 2]
    left = [x for x in array if pivot in rules_inv[x]]
    middle = [x for x in array if x == pivot]
    right = [x for x in array if pivot in rules[x]]

    return quicksort(left) + middle + quicksort(right)


def sort_and_get_middle(update: list) -> int:
    return get_middle(quicksort(update))


collecting_rules = True
for line in open("./input.txt").readlines():
    if collecting_rules:
        # Detect end of rules
        if line == '\n':
            collecting_rules = False
            for first in rules.keys():
                for second in rules[first]:
                    rules_inv[second].add(first)
            continue

        # First collect page ordering rules
        ## e.g. 47|53 = if both pages 47 and 53, then i_47 < i_53
        first, second = line.strip().split('|')
        rules[first].add(second)
    else:
        # Second collect page numbers of each update
        ## e.g. 75,47,61,53,29 is those page numbers
        update = line.strip().split(',')
        seen = set()
        for page in update:
            # If we've seen a page that should follow the current one, abort
            if seen & rules[page]:
                # Sort update correctly, take middle value for solution B
                solution_b += sort_and_get_middle(update)
                break
            seen.add(page)
        else:
            # Update is value, update A
            solution_a += get_middle(update)

print(f"A: {solution_a}")
print(f"B: {solution_b}")

