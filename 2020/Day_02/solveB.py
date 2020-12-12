#!/usr/bin/env python3

import re

from collections import Counter


def validate_pwd(idx_a, idx_b, char, seq):
    return Counter([seq[idx_a-1], seq[idx_b-1]])[char] == 1


if __name__ == '__main__':
    with open('input.txt') as f:
        valid_counts = 0
        for line in f.readlines():
            start_idx, end_idx, character, pwd = re.search(r'(\d+)-(\d+) (\w): (\w+)', line).groups()
            valid_counts += validate_pwd(int(start_idx), int(end_idx), character, pwd)
        print(valid_counts)
