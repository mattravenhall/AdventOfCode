#!/usr/bin/env python3

import re

from collections import Counter


def validate_pwd(min_range, max_range, char, seq):
    return min_range <= Counter(seq)[char] <= max_range


if __name__ == '__main__':
    with open('input.txt') as f:
        valid_counts = 0
        for line in f.readlines():
            range_min, range_max, character, pwd = re.search(r'(\d+)-(\d+) (\w): (\w+)', line).groups()
            valid_counts += validate_pwd(int(range_min), int(range_max), character, pwd)
        print(valid_counts)
