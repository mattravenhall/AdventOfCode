#!/usr/bin/env python3

import math
from itertools import combinations
from operator import add


def calc_area(
    vector_a: tuple[int, int],
    vector_b: tuple[int, int],
) -> int:
    x = abs(vector_a[0] - vector_b[0]) + 1
    y = abs(vector_a[1] - vector_b[1]) + 1
    return x * y


def area_contains_edges(corner_a: tuple[int, int], corner_b: tuple[int, int], edges: set) -> bool:
    """Return true if not border tiles of area are edges"""
    x = (
        min(corner_a[0], corner_b[0])+1,
        max(corner_a[0], corner_b[0])-1,
    )
    y = (
        min(corner_a[1], corner_b[1])+1,
        max(corner_a[1], corner_b[1])-1,
    )
    for edge in edges:
        if (x[0] <= edge[0] <= x[1]) and (y[0] <= edge[1] <= y[1]):
            return True
    return False


def solve(path: str) -> int:
    points = list(tuple(map(int, line.strip().split(','))) for line in open(path).readlines())
   
    # Part One: Identify Max Area
    areas = set()
    max_area = -1
    max_green_area = -1
    for a, b in combinations(set(points), r=2):
        area = calc_area(a, b)
        areas.add((area, a, b))
        if area > max_area:
            max_area = area
    
    # Part Two: Identify Largest Tiled Area
    tiles = {
        "corner": set(),
        "edge": set(),
        "inside": set(),
    }
    # Draw polygon
    for a, b in zip(points, points[1:]+[points[0]]):
        tiles["corner"].add(a)
        axis = int(a[1] == b[1])
        delta = int(not axis)
        start = min(a[delta], b[delta])+1
        end = max(a[delta], b[delta])
        for i in range(start, end):
            tile = [None, None]
            tile[axis] = a[axis]
            tile[delta] = i
            tiles["edge"].add(tuple(tile))
    
    # Check areas from largest to smallest
    areas = sorted(areas, key=lambda x: x[0])[::-1]
    max_tiled_area = None
    max_x, max_y = 0, 0
    for point in points:
        if point[0] > max_x:
            max_x = point[0]
        if point[1] > max_y:
            max_y = point[1]
    
    for area, a, b in areas:
        if not area_contains_edges(a, b, tiles["edge"]):
            max_tiled_area = area
            break

    return max_area, max_tiled_area


assert solve("test.txt") == (50, 24)

print(solve("input.txt"))
