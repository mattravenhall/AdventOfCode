#!/usr/bin/env python3

import os
import re

from collections import defaultdict

tree = defaultdict(set)

with open('input.txt') as f:
    for line in f.readlines():
        # Collect parent-child relations
        pattern = r'(\w+\s\w+) bags contain (\d+ \w+ \w+) bags?,?.?)+'
        parent_raw, children_raw = line.strip().split('contain')

        parent = re.search(r'(\w+ \w+) bags', parent_raw).groups()[0]
        children = re.findall(f'(\d+) (\w+ \w+) bags?', children_raw)

        for num_child in children:
            tree[parent].add(num_child)


def sum_bags(parent, tree, count=0):
    # Count descendant bags
    children = tree[parent]
    if children == set():
        # If leaf node, return 1
        return 0
    for num, child in children:
        num_desc = sum_bags(child, tree)
        num = int(num)
        count += (num * num_desc) + num
    return count


total_bags = sum_bags('shiny gold', tree)
print(f"{total_bags} bags")
