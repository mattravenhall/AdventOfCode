#!/usr/bin/env python3

with open('input.txt') as f:
    values = {int(value) for value in f.readlines()}
    for value in values:
        if (2020-value) in values:
            print(f"Solution found: {value}*{2020-value}={value*(2020-value)}")
            break