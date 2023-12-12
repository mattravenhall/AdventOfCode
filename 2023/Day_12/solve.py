#!/usr/bin/env python3

from functools import lru_cache


@lru_cache
def count_arrangements(line: str, groups: tuple[int]) -> int:
    if len(line) == 0 or set(line) == {'.'}:
        return int(len(groups) == 0)
    if line[0] == '.':
        return count_arrangements(line.lstrip('.'), groups)
    elif line[0] == '?':
        return count_arrangements(line[1:], groups) + count_arrangements('#'+line[1:], groups)
    elif line[0] == '#':
        if (not groups) \
            or ('.' in line[:groups[0]]) \
            or (len(line) < groups[0]):
            return 0
        if (len(groups) > 1):
            if (len(line) < (sum(groups) + len(groups)) - 1) or (line[groups[0]] == '#'):
                return 0
        if len(groups) > 1 and line[groups[0]] == '?':
            return count_arrangements(line[groups[0]+1:], groups[1:])
        else:
            return count_arrangements(line[groups[0]:], groups[1:])
    else:
        raise ValueError(f"Unexpected character '{line[0]}'")


assert count_arrangements("???.###", (1,1,3,)) == 1
assert count_arrangements(".??..??...?##.", (1,1,3,)) == 4
assert count_arrangements("?#?#?#?#?#?#?#?", (1,3,1,6,)) == 1
assert count_arrangements("????.#...#...", (4,1,1,)) == 1
assert count_arrangements("????.######..#####.", (1,6,5,)) == 4
assert count_arrangements("?###????????", (3,2,1,)) == 10

assert count_arrangements('?'.join(5*["???.###"]), 5*(1,1,3,)) == 1
assert count_arrangements('?'.join(5*[".??..??...?##."]), 5*(1,1,3,)) == 16384
assert count_arrangements('?'.join(5*["?#?#?#?#?#?#?#?"]), 5*(1,3,1,6,)) == 1
assert count_arrangements('?'.join(5*["????.#...#..."]), 5*(4,1,1,)) == 16
assert count_arrangements('?'.join(5*["????.######..#####."]), 5*(1,6,5,)) == 2500
assert count_arrangements('?'.join(5*["?###????????"]), 5*(3,2,1,)) == 506250


total_arrangements_A = 0
total_arrangements_B = 0
for line in open("input.txt").readlines():
    line = line.strip()
    if line[0] == '|':
        continue
    sections, sizes = line.strip().split()
    sizes = tuple(map(int, sizes.split(',')))
    
    total_arrangements_A += count_arrangements(sections, sizes)
    total_arrangements_B += count_arrangements('?'.join(5*[sections]), 5*sizes)

print(total_arrangements_A)
print(total_arrangements_B)
