#!/usr/bin/env python3

def solve_a(sequence: str) -> int:
    total = 0
    for bank in sequence.split():
        batteries = list(map(int, list(bank.strip())))
        digits = [None, None]
        digits[0] = max(batteries[:-1])
        digits[1] = max(batteries[batteries.index(digits[0])+1:])
        value = int(''.join(map(str, digits)))
        total += value
    return total


def solve_b(sequence: str) -> int:
    total = 0
    n_batteries = 12

    for bank in sequence.split():
        batteries = list(map(int, list(bank.strip())))
        solution = ""
        for seq_len in range(n_batteries, 0, -1):
            searchable = batteries[:len(batteries)-seq_len+1]
            battery = max(searchable)
            index = batteries.index(battery)
            solution += str(battery)
            batteries = batteries[index+1:]
        total += int(solution)
    return total


test_input = """987654321111111
811111111111119
234234234234278
818181911112111
"""

assert solve_a(test_input) == 357
assert solve_b(test_input) == 3121910778619

print(f"A: {solve_a(open('input.txt').read())}")
print(f"B: {solve_b(open('input.txt').read())}")

