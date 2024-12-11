#!/usr/bin/env python3

from copy import deepcopy
from functools import cache


class Stones():
    def __init__(self, input_file: str) -> None:
        self.stones = self._parse_input(input_file)

    def _parse_input(self, input_file: str) -> list[str]:
        return open(input_file).readlines()[0].strip().split()

    @staticmethod
    @cache
    def _perform_blink(stone: str) -> list[str]:
        """This is the slow implementation, it's fine for part one."""
        if stone == '0':
            return ['1']
        elif len(stone) % 2 == 0:
            return [
                stone[:len(stone)//2],
                str(int(stone[len(stone)//2:])),
            ]
        else:
            return [str(int(stone) * 2024)]

    @cache
    def _perform_blink_count(self, stone: str, blinks: int) -> int:
        """This is the fast implementation, it's needed for part two."""

        if blinks == 0:
            return 1
        elif stone == '0':
            return self._perform_blink_count('1', blinks - 1)
        elif len(stone) % 2 == 0:
            left = self._perform_blink_count(stone[:len(stone)//2], blinks - 1)
            right = self._perform_blink_count(str(int(stone[len(stone)//2:])), blinks -1)
            return left + right
        else:
            return self._perform_blink_count(str(int(stone) * 2024), blinks - 1)

    def solve(self, blinks: int, fast: bool = False) -> int:
        """Solve for a given input.

        Args:
            blinks (int): Number of blink steps to perform.
            fast (bool, optional): If True, we'll disregard the sequence and just calculate counts. Defaults to False.

        Returns:
            int: Number of stones remaining after all blinks.
        """
        old_stones: list[str] = deepcopy(self.stones)

        if blinks == 0:
            return len(old_stones)

        if not fast:
            # Slow
            for i in range(blinks):
                new_stones: list[str] = []
                for stone in old_stones:
                    new_stones.extend(self._perform_blink(stone))
                old_stones = new_stones
            return len(new_stones)

        else:
            # Fast
            return sum(self._perform_blink_count(stone, blinks) for stone in self.stones)


assert Stones("test.txt").solve(blinks=0) == 2
assert Stones("test.txt").solve(blinks=1) == 3
assert Stones("test.txt").solve(blinks=2) == 4
assert Stones("test.txt").solve(blinks=3) == 5
assert Stones("test.txt").solve(blinks=4) == 9
assert Stones("test.txt").solve(blinks=5) == 13
assert Stones("test.txt").solve(blinks=6) == 22
assert Stones("test.txt").solve(blinks=25) == 55312

print(f"A: {Stones('input.txt').solve(blinks=25)}")
print(f"B: {Stones('input.txt').solve(blinks=75, fast=True)}")
