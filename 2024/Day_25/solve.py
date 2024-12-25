#!/usr/bin/env python3

class KeyLockChecker:
    def __init__(self, input_file: str = None) -> None:
        self.keys, self.locks = self._parse_input(input_file)

    def _parse_input(self, input_file: str) -> tuple[list, list]:
        keys = []
        locks = []
        for grid in open(input_file).read().split('\n\n'):
            rows = grid.strip().split('\n')
            heights = [None, None, None, None, None]
            if rows[0] == '#####':
                # Parse as a lock
                for i, columns in enumerate(rows):
                    for j, space in enumerate(columns):
                        if heights[j] is None and space == '.':
                            heights[j] = i - 1
                locks.append(heights)
            elif rows[-1] == '#####':
                # Parse as a key
                for i, columns in enumerate(rows[::-1]):
                    for j, space in enumerate(columns):
                        if heights[j] is None and space == '.':
                            heights[j] = i - 1
                keys.append(heights)
            else:
                ValueError(f"Unknown grid format")

        return keys, locks

    def count_nonoverlapping(self):
        total = 0
        for lock in self.locks:
            for key in self.keys:
                # print(f"Checking {lock=} with {key=}")
                for column in range(5):
                    if key[column] + lock[column] >= 6:
                        # print(f"Clash at {column=}")
                        break
                else:
                    # print("Valid fit")
                    total += 1
        return total


assert KeyLockChecker("./test.txt").count_nonoverlapping() == 3

print(f"A: {KeyLockChecker('./input.txt').count_nonoverlapping()}")
