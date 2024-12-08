#!/usr/bin/env python3

from collections import defaultdict
from copy import deepcopy
from itertools import combinations
from typing import Optional

solution_a = 0
solution_b = 0

class Grid():
    def __init__(self, input_file: str):
        self.grid: list[list[str]] = []
        self.antennae: dict = defaultdict(set)

        # Build grid
        for i, line in enumerate(open(input_file).readlines()):
            if line == "":
                continue
            line = list(line.strip())
            self.grid.append(line)

            # Locate antennae
            for j, tile in enumerate(line):
                if tile != '.':
                    self.antennae[tile].add((i, j))

    def _out_of_range(self, x, y) -> bool:
        if x < 0 or y < 0 or x >= len(self.grid) or y >= len(self.grid[0]):
            return True
        else:
            return False

    @staticmethod
    def _vector_add(x: tuple, y: tuple) -> tuple:
        return tuple(map(sum, zip(x, y)))

    def _identify_candidates(self, x: tuple[int], y: tuple[int], infinite=False) -> tuple[int]:
        distance = (x[0] - y[0], x[1] - y[1])

        if infinite:
            # TODO: Keep going until out of range
            candidates = set()
            
            candidate_pos = x
            while not self._out_of_range(*candidate_pos):
                candidates.add(candidate_pos)
                candidate_pos = (
                    candidate_pos[0] + distance[0],
                    candidate_pos[1] + distance[1],
                )

            candidate_neg = y
            while not self._out_of_range(*candidate_neg):
                candidates.add(candidate_neg)
                candidate_neg = (
                    candidate_neg[0] - distance[0],
                    candidate_neg[1] - distance[1],
                )
            # candidates -= {x, y}
        else:
            candidates = [
                candidate
                for candidate
                in
                [(
                    x[0] + distance[0],
                    x[1] + distance[1],
                ),
                (
                    y[0] - distance[0],
                    y[1] - distance[1],
                )]
                if not self._out_of_range(*candidate)
            ]
            
        return candidates

    def _draw_grid(self, antinodes: Optional[set] = None):
        view = deepcopy(self.grid)

        for x, y in antinodes:
            view[x][y] = '#'
            
        print('\n'.join([''.join(x) for x in view]))

    def locate_antinodes_a(self, debug: bool = False) -> int:
        antinodes: set = set()
        for frequency in self.antennae.keys():
            # Get pairs of antennae locations
            pairs = combinations(self.antennae[frequency], 2)

            for loc_a, loc_b in pairs:
                # Identify possible antinode locations (2x distance between)
                candidates = self._identify_candidates(loc_a, loc_b)
                for candidate in candidates:
                    # If in range, add to antinodes
                    if not self._out_of_range(*candidate):
                        antinodes.add(candidate)
        
        # Debugging
        if debug:
            self._draw_grid(antinodes)

        return len(antinodes)

    def locate_antinodes_b(self, debug: bool = False) -> int:
        # Now distance is infinite
        # Also, locations with > antinode also emit antinodes?

        antinodes: dict = defaultdict(set)  # antinode: freq
        t_antennae: set = set()
        for frequency in self.antennae.keys():
            # Get pairs of antennae locations
            pairs = combinations(self.antennae[frequency], 2)

            for loc_a, loc_b in pairs:
                # Identify possible antinode locations (2x distance between)
                candidates = self._identify_candidates(loc_a, loc_b, infinite=True)
                for candidate in candidates:
                    # If in range, add to antinodes
                    if not self._out_of_range(*candidate):
                        antinodes[candidate].add(frequency)
                        if len(antinodes[candidate]) >= 2:
                            t_antennae.add(candidate)

        # Debugging
        if debug:
            self._draw_grid(antinodes)

        return len(antinodes.keys())


print(f"A: {Grid('./test.txt').locate_antinodes_a()}")
print(f"B: {Grid('./input.txt').locate_antinodes_b()}")
