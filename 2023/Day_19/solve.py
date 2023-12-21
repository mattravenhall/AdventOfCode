#!/usr/bin/env python3

from collections import defaultdict
import copy
import heapq
import math
from multiprocessing import Pool
import re


def part_is_accepted(workflows: dict, x: str, m: str, a: str, s: str) -> bool:
    destination = 'in'
    while destination not in {'A', 'R'}:
        for condition, next_destination in workflows[destination]:
            if eval(condition):
                destination = next_destination
                break
    return destination == 'A'


def solve(filename: str) -> int:
    workflows = defaultdict(list)
    workflows_processed = False
    accepted = {key: 0 for key in 'xmas'}

    # Log corresponding splits for part two
    ranges = {c: {0, 4000} for c in 'xmas'}
    counts = {c: 0 for c in 'xmas'}

    for line in open(filename).readlines():
        line = line.strip()
        if line == '':
            workflows_processed = True

            # Part Two
            queue = [(
                'in',
                list({
                    'x': [1, 4000],
                    'm': [1, 4000],
                    'a': [1, 4000],
                    's': [1, 4000],   # convert this to a dict when needed
                }.items())
            )]
            heapq.heapify(queue)
            acceptable_combinations = 0
            while queue:
                workflow, ranges = queue.pop()

                if workflow == 'R' or any([low > high for _, (low, high) in ranges]):
                    # Ignore rejected parts
                    continue
                elif workflow == 'A':
                    # Update combinations with combinations from current state
                    acceptable_combinations += math.prod([
                        high - low + 1
                        for _, (low, high) in ranges
                    ])
                    continue

                for condition, result in workflows[workflow]:
                    if condition == 'True':  # A, R, and default workflow changes
                        queue.append((result, ranges))
                        continue
                    else:
                        # If a condition exists, add states for true and false
                        variable, op, value = re.findall(r'^([xmas])([<>])(\d+)', condition)[0]
                        value = int(value)
                        ranges_dict = dict(ranges)
                        ranges_true = copy.deepcopy(ranges_dict)
                        ranges_false = copy.deepcopy(ranges_dict)

                        if op == '>':
                            ranges_true[variable][0] = max(ranges_dict[variable][0], value + 1)
                            ranges_false[variable][1] = min(ranges_dict[variable][1], value)
                        elif op == '<':
                            ranges_true[variable][1] = min(ranges_dict[variable][1], value - 1)
                            ranges_false[variable][0] = max(ranges_dict[variable][0], value)
                        else:
                            raise ValueError("Unexpected operator: '{op}'")

                        # Add new state for condition is true
                        queue.append((result, list(ranges_true.items())))

                        # Update state for condition is false
                        ranges = list(ranges_false.items())

        elif not workflows_processed:
            # Part one
            name, workflow = line.strip('}').split('{')
            for section in workflow.split(','):
                if ':' not in section:
                    workflows[name].append(('True', section))
                else:
                    condition, destination = section.split(':')
                    workflows[name].append((condition, destination))
            
            # Part two
            splits = re.findall(r'([xmas])([<>])(\d+):', line)
            for c, op, value in splits:
                ranges[c].add(int(value)-(op == '<'))

        else:
            for variable, value in re.findall(r'([xmas])=(\d+)', line):
                globals()[variable] = int(value)

            if part_is_accepted(workflows, *[globals()[i] for i in 'xmas']):
                for key in 'xmas':
                    accepted[key] += globals()[key]

    return sum(accepted.values()), acceptable_combinations

assert solve("test.txt") == (19114, 167409079868000), f"Error: {solve('test.txt')} != (19114, 167409079868000)"

part_one, part_two = solve("input.txt")

print(part_one)
print(part_two)
