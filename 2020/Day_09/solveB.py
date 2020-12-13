#!/usr/bin/env python

import sys

filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
digits = [int(line.strip()) for line in open(filename).readlines()][::-1]

total = 530627549


for i in range(len(digits)):
    # Skip the massive digits
    if (digits[i] > total) or (digits[i] == total):
        continue

    digit_bag = [digits[i]]
    mod = 1
    while sum(digit_bag) < total:
        digit_bag.append(digits[i+mod])
        mod += 1

    if sum(digit_bag) == total:
        print(min(digit_bag)+max(digit_bag))
        sys.exit()

