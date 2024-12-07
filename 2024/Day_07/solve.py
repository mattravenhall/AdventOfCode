#!/usr/bin/env python3

from itertools import product
from math import prod


def concat(values: list) -> int:
    return int(''.join(map(str, values)))


def solve(path_input: str, operations: list) -> int:
    solution = 0
    for i, line in enumerate(open(path_input).readlines()):
        goal, inputs = line.strip().split(':')
        goal = int(goal)
        inputs = list(map(int, inputs.split()))

        # Check combinations
        gaps = len(inputs) - 1
        for order_of_operations in product(operations, repeat=gaps):
            # print(f"{order_of_operations=}, {inputs=}")
            total = inputs[0]
            for i, input in enumerate(inputs[1:]):
                total = order_of_operations[i]([total, input])
                # print(f"{i=} {input=} {order_of_operations[i]=} {total=}")
                if total > goal:
                    # print("exceeded goal")
                    break
            if total == goal:
                # print(f"POSSIBLE with {inputs=} {order_of_operations=}")
                solution += goal
                break
        # else:
        #     print(f"NOT POSSIBLE with {inputs=} {order_of_operations=}")
    return solution


path_input = "./input.txt"
print(f"A: {solve(path_input, operations=[sum, prod])}")
print(f"B: {solve(path_input, operations=[sum, prod, concat])}")
