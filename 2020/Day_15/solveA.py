#!/usr/bin/env python


def find_nth_value(init_seq, nth=2020):
    sequence = [int(s) for s in init_seq.split(',')]
    len_init_seq = len(sequence)

    last_seen = {digit: i+1 for i, digit in enumerate(sequence[:-1])}

    last_digit = sequence[-1]
    for turn in range(len_init_seq, nth):
        if last_digit not in last_seen.keys():
            next_digit = 0
        else:
            next_digit = turn - last_seen[last_digit]
        last_seen[last_digit] = turn
        last_digit = next_digit
    return last_digit


init_seq = "19,0,5,1,10,13"

assert find_nth_value("0,3,6") == 436, "Failure on test input"
assert find_nth_value("1,3,2") == 1, "Failure on test input"
assert find_nth_value("2,1,3") == 10, "Failure on test input"
assert find_nth_value("1,2,3") == 27, "Failure on test input"
assert find_nth_value("2,3,1") == 78, "Failure on test input"
assert find_nth_value("3,2,1") == 438, "Failure on test input"
assert find_nth_value("3,1,2") == 1836, "Failure on test input"

print(find_nth_value(init_seq))
