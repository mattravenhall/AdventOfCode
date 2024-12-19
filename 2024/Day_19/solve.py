#!/usr/bin/env python3

import logging
from functools import cache


class Solver:
    def __init__(self, input_file: str) -> tuple[list, list[str]]:
        self.towels, self.designs = self._parse_input(input_file)
    
    def _parse_input(self, input_file: str):
        towels, designs = open(input_file).read().split("\n\n")
        towels = towels.split(', ')
        designs = designs.strip().split('\n')
        return towels, designs

    @cache
    def _design_is_valid(self, design: str) -> int:
        valid_sequences = 0
        for towel in self.towels:
            if design.startswith(towel):
                seq_remaining = design[len(towel):]
                if seq_remaining == '':
                    valid_sequences += 1
                else:
                    valid_sequences += self._design_is_valid(seq_remaining)
        return valid_sequences
    
    def count_valid_designs(self) -> int:
        total = 0
        for design in self.designs:
            total += bool(self._design_is_valid(design))
        return total

    def find_valid_designs(self) -> tuple[int, int]:
        combinations = {}
        for design in self.designs:
            combinations[design] = self._design_is_valid(design)

        n_valid = sum(map(bool, combinations.values()))
        n_combinations = sum(combinations.values())
        return n_valid, n_combinations

test_solver = Solver("./test.txt")
assert test_solver.find_valid_designs() == (6, 16)

solver = Solver("./input.txt")
solution_a, solution_b = solver.find_valid_designs()
print(f"A: {solution_a}")  # 358
print(f"B: {solution_b}")  # 600639829400603
