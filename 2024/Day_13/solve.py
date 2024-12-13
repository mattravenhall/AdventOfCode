#!/usr/bin/env python3.11

import re

re_button = r"Button (A|B): X\+(\d+), Y\+(\d+)"
re_prize = r"Prize: X=(\d+), Y=(\d+)"

class ClawMachine():
    costs: dict = {
        "A": 3,
        "B": 1,
    }

    def __init__(self, input_file: str) -> None:
        self.machines = self._parse_input(input_file)

    def _parse_input(self, input_file: str) -> list[str]:
        #[ [ A, B, Prize ], ...]
        machines: list[list[tuple[tuple[int, int], tuple[int, int]], tuple[int, int]]] = []
    
        machine = []
        for line in open(input_file).readlines():
            line = line.strip()
            if line.startswith("Button "):
                _, x, y = re.match(re_button, line).groups()
                machine.append((int(x), int(y)))
            elif line.startswith("Prize: "):
                x, y = re.match(re_prize, line).groups()
                machine.append((int(x), int(y)))
            elif line == "":
                continue
            else:
                breakpoint()
            
            if len(machine) == 3:
                machines.append(tuple(machine))
                machine = []

        return machines

    @staticmethod
    def _vector_add(x: tuple, y: tuple) -> tuple:
        return tuple(map(sum, zip(x, y)))

    @staticmethod
    def _cramers_rule(x: tuple[int, int], y: tuple[int, int], prize: tuple[int, int]):
        det_prize = (x[0] * y[1]) - (y[0] * x[1])

        det_x = (prize[0] * y[1]) - (y[0] * prize[1])
        det_y = (x[0] * prize[1]) - (prize[0] * x[1])

        X = det_x / det_prize
        Y = det_y / det_prize

        return X, Y

    def solve_machine(self, a: tuple[int, int], b: tuple[int, int], prize: tuple[int, int]) -> int:
        presses_a, presses_b = self._cramers_rule(a, b, prize)

        if presses_a.is_integer() and presses_b.is_integer():
            return (self.costs["A"] * int(presses_a)) + (self.costs["B"] * int(presses_b))
        else:
            return -1

    def solve(self, adjust_prize: int = 0) -> tuple[int, int]:
        wins = 0
        total_cost = 0
        for vec_a, vec_b, prize in self.machines:
            cost = self.solve_machine(vec_a, vec_b, self._vector_add(prize, [adjust_prize, adjust_prize]))
            if cost > -1:
                wins += 1
                total_cost += cost
        return wins, total_cost

assert ClawMachine("./test.txt").solve() == (2, 480)

print(f"A: {ClawMachine('./input.txt').solve()[1]}")
print(f"B: {ClawMachine('./input.txt').solve(adjust_prize=10000000000000)[1]}")
