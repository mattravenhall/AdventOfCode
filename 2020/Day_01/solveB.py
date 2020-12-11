#!/usr/bin/env python3

# Unsophisticated, but quick enough for it not to matter
with open('input.txt') as f:
    values = {int(value) for value in f.readlines()}
    for value_i in values:
        for value_j in values:
            for value_k in values:
                if (value_i + value_j + value_k) == 2020:
                    print(f"Solution found: {value_i}*{value_j}*{value_k}={value_i*value_j*value_k}")
                    import sys; sys.exit()
