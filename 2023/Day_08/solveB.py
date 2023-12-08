#!/usr/bin/env python3

from collections import defaultdict
import math
import re

re_nodes = r"([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)"

nodes: dict[tuple] = {}
path = None
a_nodes = set()
z_nodes = set()


def count_traversal(node: str, path: list[str]):
    count = 0
    assert not set(path) - {'L', 'R'}, "Invalid path"

    while not node.endswith('Z'):
        step = path[count % len(path)]
        count += 1
        node = nodes[node][0 if step == 'L' else 1]
    return count


# Populate nodes
for line in open("input.txt").readlines():
    if path is None:
        path = list(line.strip())
    elif line == '\n':
        continue
    else:
        node, child_left, child_right = re.search(re_nodes, line).groups()
        if node.endswith('A'):
            a_nodes.add(node)
        elif node.endswith('Z'):
            z_nodes.add(node)
        nodes[node] = (child_left, child_right)

# Get all shortest paths
counts = [
    count_traversal(
        node = node,
        path = path,
    )
    for node in a_nodes
]

# Find LCM
print(math.lcm(*counts))
