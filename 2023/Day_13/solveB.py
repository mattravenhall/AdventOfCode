#!/usr/bin/env python3

from typing import Optional


def process_pattern(pattern: list[list[str]]) -> int:
    def _find_symmetry(pattern: list[list[str]]) -> Optional[int]:
        for i in range(len(pattern)-1):
            location = j = i+1
            differences = 0
            while 0 <= i <= len(pattern)-2 and 1 <= j <= len(pattern)-1:
                differences += sum([x!=y for x, y in zip(pattern[i], pattern[j])])
                i -= 1
                j += 1
            if differences == 1:
                return location

    # Consider horizontal reflections
    row_score = _find_symmetry(pattern)
    if row_score is not None:
        print(f"Pattern found on row {row_score}")
        return row_score * 100

    # Consider vertical reflections
    pattern = list(map("".join, zip(*reversed(pattern))))
    col_score = _find_symmetry(pattern)
    if col_score is not None:
        print(f"Pattern found on col {col_score}")
        return col_score
    
    return 0


total = 0
pattern = []
for line in open("input.txt").readlines()+['']:
    line = line.strip()
    if line == '':
        # Process pattern and refresh
        total += process_pattern(pattern)
        pattern = []
    else:
        pattern.append(line)

print(total)
