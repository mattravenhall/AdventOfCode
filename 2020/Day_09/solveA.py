#!/usr/bin/env python3

import sys

filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
digits = [int(line.strip()) for line in open(filename).readlines()]

preamble = 25


def find_sum_pair(total, digits):
    for digit in digits:
        if (total - digit) in digits:
            return digit, total-digit
    return False


for i in range(preamble, len(digits)):
    total = digits[i]
    pre_digits = digits[i-preamble:i]

    if not find_sum_pair(total, pre_digits):
        print(total)
        exit
