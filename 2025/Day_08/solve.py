#!/usr/bin/env python3.11

import math
from collections import defaultdict
from itertools import combinations


def euc_distance(
    vector_a: tuple[int, int, int], 
    vector_b: tuple[int, int, int],
) -> int:
    sum_of_squared_diffs = sum((a - b) ** 2 for a, b in zip(vector_a, vector_b))

    return math.sqrt(sum_of_squared_diffs)


def solve(path: str, connections: int) -> int:
    points = set()
    for line in open(path).readlines():
        points.add(tuple(map(int, line.strip().split(','))))
    
    distances = set()
    for vector_a, vector_b in combinations(points, 2):
        distances.add((euc_distance(vector_a, vector_b), tuple(sorted([vector_a, vector_b]))))

    # Sort pairs from closest to furthest
    distances = sorted(distances, key=lambda x: x[0])

    # Start collecting
    membership = {}
    new_circuit_id = 0

    # Connect the closest 1000 pairs
    n_connections = 0
    while distances:
        distance, (box_a, box_b) = distances.pop(0)
        mem_a = membership.get(box_a)
        mem_b = membership.get(box_b)

        match [mem_a, mem_b]:
            case [None, None]:
                membership[box_a] = new_circuit_id
                membership[box_b] = new_circuit_id
                new_circuit_id += 1
            case [a, None]:
                membership[box_b] = a
            case [None, b]:
                membership[box_a] = b
            case _:
                if mem_a != mem_b:
                    # Merge circuits into circuit a
                    for box, circuit in membership.items():
                        if circuit == mem_b:
                            membership[box] = mem_a

        n_connections += 1

        # Detect conditions required for part one (max connections)
        if n_connections == connections:
            membership_at_checkpoint = membership.copy()
  
        # Detect conditions required for part two (all boxes in one circuit)
        if len(membership.keys()) == len(points) and len(set(membership.values())) == 1:
            answer_b = box_a[0] * box_b[0]
            break

    # Solve for part one
    # Invert memberships to get their sizes
    circuits = defaultdict(set)
    for point, circuit in membership_at_checkpoint.items():
        circuits[circuit].add(point)
    circuits = dict(circuits)

    # Get circuit sizes
    sizes = {}
    for circuit, members in circuits.items():
        sizes[circuit] = len(members)

    answer_a = math.prod(sorted(sizes.values())[-3:])
    
    return answer_a, answer_b


assert solve("test.txt", connections=10) == (40, 25272)

print(solve("input.txt", connections=1000))
