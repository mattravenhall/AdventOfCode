#!/usr/bin/env python3

from collections import defaultdict
import re

re_nodes = r"([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)"

nodes: dict[tuple] = {}
path = None


def count_traversal(node: str, path: list[str], destination: str = 'ZZZ'):
    count = 0
    assert not set(path) - {'L', 'R'}, "Invalid path"

    while node != destination:
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
        nodes[node] = (child_left, child_right)

print(count_traversal(
    node = 'AAA',
    path = path,
))
