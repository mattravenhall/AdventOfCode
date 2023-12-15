#!/usr/bin/env python3

from collections import defaultdict, OrderedDict
import re


def find_hash(string: str) -> int:
    """
    1. Determine the ASCII code for the current character of the string.
    2. Increase the current value by the ASCII code you just determined.
    3. Set the current value to itself multiplied by 17.
    4. Set the current value to the remainder of dividing itself by 256.
    """
    total = 0
    for char in string:
        total += ord(char)
        total *= 17
        total %= 256
    return total


assert find_hash('HASH') == 52

boxes = defaultdict(OrderedDict)
input = open("input.txt").readlines()[0].strip()
result_part_1 = 0
result_part_2 = 0

# Process input
for string in input.split(','):
    # Part 1
    result_part_1 += find_hash(string)

    # Part 2
    new_label, new_lens = re.search(r'^(.*)[-=](\d+)?$', string).groups()
    box_id = find_hash(new_label)
    if '-' in string:
        # Remove lens from box, if present
        if new_label in boxes[box_id]:
            boxes[box_id].pop(new_label)
    elif '=' in string:
        # Update lens for given label
        new_lens = int(new_lens)
        boxes[box_id][new_label] = new_lens

# Calculate scores for part 2
for box_id in range(256):
    for slot_id, (label, lens) in enumerate(boxes[box_id].items()):        
        score = ((box_id + 1) * (slot_id + 1) * lens)
        # print(f"[{box_id=}-{slot_id=}] {label=} {lens=} = {score}")
        result_part_2 += score

print(f"{result_part_1=}")
print(f"{result_part_2=}")
