#!/usr/bin/env python3

from collections import defaultdict
from operator import add


class Solver:
    def __init__(self, filepath: str) -> None:
        # Load garden into memory
        garden: list[list[str]] = []
        self.reachable: defaultdict(set) = defaultdict(set)
        self.rocks: set[tuple[int]] = set()
        self.visited: set[tuple[int]] = set()

        for r, line in enumerate(open(filepath).readlines()):
            row = list(line.strip())
            garden.append(row)

            for c, col in enumerate(row):
                if col == '#':
                    self.rocks.add((r, c))
                elif col == 'S':
                    self.start = (r, c)
        
        self.garden = garden
        self.limits = (r, c)

    @staticmethod
    def _vec_add(vec_a: tuple[int], vec_b: tuple[int]) -> tuple[int]:
        """Allow each addition of vectors"""
        return tuple(map(add, vec_a, vec_b))

    def _in_bounds(self, position: tuple[int]) -> bool:
        """Check whether a position vector is within the given bound"""
        return (0 <= position[0] < self.limits[0]) and (0 <= position[1] < self.limits[1])

    def visit_plots_in_range(self, position: tuple[int], steps: int = 0, range: int = 64) -> None:
        """Part One: Collect number of valid spaces within 64 steps"""

        space = self.garden[position[0]][position[1]]

        if steps > range or space in self.rocks or position in self.reachable[steps] or not self._in_bounds(position):
            # If space is invalid or range is reached, return count
            return
        else:
            # If space is valid, add to visited spaces
            self.visited.add(position)
            self.reachable[steps].add(position)

        # Recurse into neighbours with reduced range
        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbour = self._vec_add(position, direction)
            if neighbour not in self.rocks:
                self.visit_plots_in_range(neighbour, steps + 1, range)
    
    def solveA(self, range: int = 64, debug: bool = False) -> int:
        self.visit_plots_in_range(self.start, 0, range)
        if debug:
            self.print_garden()
        
        return len(self.reachable[range])
    
    def print_garden(self) -> None:
        for r, row in enumerate(self.garden):
            line = ''
            for c, col in enumerate(row):
                if (r, c) in self.visited:
                    line += 'O'
                elif (r, c) in self.rocks:
                    line += '#'
                else:
                    line += '.'
            print(line)


tester = Solver("test.txt")
assert tester.solveA(6) == 16, "Test case broken"

solver = Solver("input.txt")
print(solver.solveA())

# breakpoint()
