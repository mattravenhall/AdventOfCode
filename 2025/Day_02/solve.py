#!/usr/bin/env python3

import re


def _id_is_invalid_a(id: int) -> bool:
    id_str = str(id)
    length = len(id_str)
    if length == 0 or length % 2:
        return False
    middle = length // 2
    return id_str[:middle] == id_str[middle:]


def _id_is_invalid_b(id: int) -> bool:
    id_str = str(id)
    length = len(id_str)
    middle = length // 2
    if length <= 1:
        return False
    if len(set(id_str)) == 1:
        return True

    # Build up a pattern (up to middle), if r'^(pattern)+$' return True
    for index in range(2, middle+1):
        pattern = id_str[:index]
        if re.match(fr"^({pattern}){{2,}}$", id_str):
            return True
    return False


def solve(sequence) -> int:
    invalid_total_a = 0
    invalid_total_b = 0
    for start, stop in map(lambda x: x.strip().split('-'), sequence.split(',')):
        for id in range(int(start), int(stop)+1):
            if _id_is_invalid_a(id):
                invalid_total_a += id
            if _id_is_invalid_b(id):
                invalid_total_b += id

    return invalid_total_a, invalid_total_b


test_input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

test_a, test_b = solve(test_input)
assert test_a == 1227775554
assert test_b == 4174379265

print(solve(open("input.txt").readlines()[0]))

