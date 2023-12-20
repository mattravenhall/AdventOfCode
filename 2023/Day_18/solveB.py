#!/usr/bin/env python3

from operator import add


def _vec_add(vec_a: tuple[int], vec_b: tuple[int]) -> tuple[int]:
    """Allow each addition of vectors"""
    return tuple(map(add, vec_a, vec_b))


def _vec_x_scalar(vector: tuple[int], scalar: int) -> tuple[int]:
    """Times a vector by a scalar"""
    return tuple(i * scalar for i in vector)


def _calc_shoelace(points: list[tuple[int]]) -> int:
    sum_a = 0
    sum_b = 0

    for i in range(len(points)-1):
        sum_a += points[i][0] * points[i+1][1]
        sum_b += points[i][1] * points[i+1][0]
    
    return abs(sum_a - sum_b) / 2


start = (0, 0)
directions = {
    "0": (0, 1),
    "1": (1, 0),
    "2": (0, -1),
    "3": (-1, 0),
}

points = [start]
previous = start
perimeter = 0
for line in open("input.txt").readlines():
    colour_code = line.split()[-1].strip('(#)')
    direction = directions[colour_code[-1]]
    distance = int(colour_code[:-1], 16)

    point = _vec_add(previous, _vec_x_scalar(direction, distance))
    points.append(point)
    previous = point
    
    perimeter += distance

inner_area = int(_calc_shoelace(points) + (perimeter / 2) + 1)

print(inner_area)  # Part two
