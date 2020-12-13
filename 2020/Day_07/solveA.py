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

        for num, child in children:
            tree[child].add(parent)


def get_holders(child, tree, colours=set()):
    child_parents = tree[child]
    if child_parents == set():
        return colours
    for child_parent in child_parents:
        colours.add(child_parent)
        colours.update(get_holders(child_parent, tree, colours))
    return colours


bag_colours = get_holders('shiny gold', tree)
print(f"{len(bag_colours)} colours")
