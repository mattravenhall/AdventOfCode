#!/usr/bin/env python3


class IntervalNode:
    def __init__(self, start, end):
        self.interval = (start, end)

        self.left = None
        self.right = None

        self.max_end = end


class IntervalTree:
    def __init__(self):
        self.root = None

    def add(self, start: int, end: int):
        new_node = IntervalNode(start, end)

        if self.root is None:
            self.root = new_node
            return

        self.root = self._add_recursive(self.root, new_node)

    def _add_recursive(self, node, new_node):
        # Update binary search tree style
        if node is None:
            return new_node

        if new_node.interval[0] < node.interval[0]:
            node.left = self._add_recursive(node.left, new_node)
        else:
            node.right = self._add_recursive(node.right, new_node)

        # Update max end to self (if leaf), of left (if exists), or of right (if exists)
        if node.left:
            node.max_end = max(node.max_end, node.left.max_end)
        if node.right:
            node.max_end = max(node.max_end, node.right.max_end)

        return node

    def value_in_tree(self, value: int) -> list:
        results = []
        self._search_tree(self.root, value, results)
        return len(results) > 0

    @staticmethod
    def _overlaps(interval: tuple[int, int], value: int) -> bool:
        return interval[0] <= value <= interval[1]

    def _search_tree(self, node, value, results):
        if node is None:
            return

        if self._overlaps(node.interval, value):
            results.append(node.interval)

        if node.left and value <= node.left.max_end:
            self._search_tree(node.left, value, results)

        if node.right and value >= node.interval[0]:
            self._search_tree(node.right, value, results)

    def display(self):
        if self.root is None:
            print("<empty tree>")

        self._display_recursive(self.root, 0)

    def _display_recursive(self, node, level):
        if node is not None:
            self._display_recursive(node.right, level + 1)
            indent = " " * level
            interval_str = f"[{node.interval[0]}, {node.interval[1]}]"
            max_end_str = f"Max: {node.max_end}"
            print(f"{indent}|-{interval_str} ({max_end_str})")
            self._display_recursive(node.left, level + 1)


def solve(path: str) -> int:
    lines = open(path).readlines()
    
    interval_tree = IntervalTree()
    fresh_ingredients = 0
    setup = True
    fresh_intervals = set()

    # Solve A: How many IDs are in the fresh intervals?
    for line in lines:
        line = line.strip()
        
        if line == '':
            setup = False
            continue

        if setup:
            interval = tuple(map(int, line.split('-')))
            fresh_intervals.add(interval)
            interval_tree.add(*interval)
            continue
        else:
            fresh_ingredients += int(interval_tree.value_in_tree(int(line)))

    # Solve B: How many IDs in the fresh intervals?
    ## Sort intervals
    fresh_intervals = sorted(fresh_intervals)
    
    ## Merge overlaps
    merged_intervals = []
    previous = None
    for interval in fresh_intervals:
        if previous is None:
            previous = sorted(interval) 
        else:
            if min(interval) <= previous[1]:
                previous[1] = max(interval[1], previous[1])
            else:
                merged_intervals.append(previous)
                previous = sorted(interval)
    merged_intervals.append(previous)
    
    ## Count IDs
    n_fresh_ids = 0
    for start, end in merged_intervals:
        n_fresh_ids += ((end - start) + 1)

    return fresh_ingredients, n_fresh_ids


assert solve("test.txt") == (3, 14)

print(solve("input.txt"))

