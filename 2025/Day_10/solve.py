#!/usr/bin/env python3

import re
from functools import reduce
from itertools import combinations
from operator import ior

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


def build_button(group: str, width: int) -> str:
    group_nums = set(map(int, group.split(',')))
    vector = []
    for i in range(width):
        vector.append(1 if i in group_nums else 0)
    #print(f"{group} -> {vector}")
    return vector


def press_buttons(states: list[tuple[int]]) -> list[int]:
    clean = lambda x: x % 2
    total = list(map(clean, (map(sum, zip(*states)))))
    return total


def solve(path: str) -> int:
    machines = []
    re_groups = r'^\[(.*)\] (\(.*\))+ {(.*)}\\n$'
    part_one = 0
    part_two = 0

    for line in open(path).readlines():
        min_size = None
        goal = list(map(int, re.findall(r"\[(.*)\]", line)[0].replace('.', '0').replace('#', '1')))
        width = len(goal)
        buttons = [
            build_button(group, width)
            for group in
            re.findall(r"\(([^)]*)\)", line)
        ]
        joltages = list(map(int, re.findall(r"{(.*)}", line)[0].split(',')))

        # Part One: Bruteforce minimal combinations needed to achieve [1] * width
        for group_size in range(1, width+1):
            for subset in combinations(buttons, group_size):
                outcome = press_buttons([x for x in subset])
                #print(f"{state=} {subset=} -> {outcome=} | {goal=}")

                if outcome == goal:
                    min_size = group_size
                    break

            if min_size is not None:
                break
        part_one += min_size

        # Part Two: Minimal presses for given joltage
        result = milp(
            [1] * len(buttons),
            constraints=LinearConstraint(np.array(buttons).T, joltages, joltages),  # Joltage to reach
            bounds=Bounds(lb=0, ub=np.inf), # Prevent negative button presses
            integrality=1   # Integers only
        ).fun
        part_two += result

    return part_one, int(part_two)


assert solve("test.txt") == (7, 33)

print(solve("input.txt"))
