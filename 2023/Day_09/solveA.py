#!/usr/bin/env python3

result = 0

def next_in_sequence(sequence: list[int]) -> int:
    differences = [sequence[i] - sequence[i-1] for i in range(1, len(sequence))]

    if len(set(differences)) == 1:
        return sequence[-1] + differences[0]
    else:
        return sequence[-1] + next_in_sequence(differences)


for line in open("input.txt").readlines():
    sequence = list(map(int, line.strip().split()))

    next_value = next_in_sequence(sequence)
    result += next_value

print(result)
