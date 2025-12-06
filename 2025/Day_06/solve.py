#!/usr/bin/env python3

from math import prod
import re
from operator import add

def solve_a(path: str) -> int:
    # Load into array
    data = []
    for line in open(path).readlines():
        data.append(line.strip().split())

    # Loop and apply operations
    operations = data[-1]
    data = data[:-1]
    total = 0
    for i, operation in enumerate(operations):
        values = map(int, [row[i] for row in data])
        match operation:
            case '+':
                total += sum(values)
            case '*':
                total += prod(values)
            case _:
                raise ValueError(f"unknown operation")
    return total


def solve_b(path: str) -> int:
    # Load into character arrow
    data = []
    for line in open(path).readlines():
        data.append(line.strip('\n'))

    # Loop and apply operators
    operations = data[-1]
    data = data[:-1]
    total = 0
    for match in re.finditer(r'[+*] +', operations): 
        start, end = match.span()
        values = []
        for column in range(end-1, start-1, -1):
            value = ''
            for row in data:
                value += row[column]
            if value.strip():
                values.append(int(value))
        
        # Apply operation to values
        match operations[start]:
            case '+':
                total += sum(values)
            case '*':
                total += prod(values)
            case _:
                raise ValueError(f"unknown operation")

    return total


assert solve_a("test.txt") == 4277556
assert solve_b("test.txt") == 3263827

print(f'A: {solve_a("input.txt")}')
print(f'B: {solve_b("input.txt")}')

