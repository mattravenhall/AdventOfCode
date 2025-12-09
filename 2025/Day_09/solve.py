#!/usr/bin/env python3

import math
from itertools import combinations


def solve(path: str) -> int:
    points = set(tuple(map(int, line.strip().split(','))) for line in open(path).readlines())
   
    # Part one: identify max area
    max_area = -1
    max_green_area = -1
    for a, b in combinations(points, r=2):
        area = calc_area(a, b)
#        print(f"{a} * {b} = {area}")
 
        if area > max_area:
            max_area = area
        
    return max_area
    

def calc_area(
    vector_a: tuple[int, int],
    vector_b: tuple[int, int],
) -> int:
    x = abs(vector_a[0] - vector_b[0]) + 1
    y = abs(vector_a[1] - vector_b[1]) + 1
    return x * y


assert solve("test.txt") == 50 #, 24

print(solve("input.txt"))
