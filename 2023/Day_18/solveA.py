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
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}

points = [start]
previous = start
perimeter = 0
for line in open("input.txt").readlines():
    direction, distance, colour_code = line.split()
    distance = int(distance)

    point = _vec_add(previous, _vec_x_scalar(directions[direction], distance))
    points.append(point)
    previous = point
    
    perimeter += distance

inner_area = int(_calc_shoelace(points) + (perimeter / 2) + 1)

print(inner_area)  # Part one
