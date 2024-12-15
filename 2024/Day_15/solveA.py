#!/usr/bin/env python3

from collections import defaultdict
import math


class RobotWarehouse():
    directions = {
        '>': (1, 0),
        '<': (-1, 0),
        '^': (0, -1),
        'v': (0, 1),
    }

    def __init__(self, input_file: str) -> None:
        self.warehouse, self.motions = self._parse_input(input_file)
        top_left = min(self.warehouse.keys())
        bottom_right = max(self.warehouse.keys())
        self.limits = {
            'x': (top_left[0], bottom_right[0]+1),
            'y': (top_left[1], bottom_right[1]+1),
        }

    def _parse_input(self, input_file: str) -> tuple[dict[tuple[int, int], str], str]:
        # Split out major components of input
        warehouse_map, motions = open(input_file).read().split('\n\n')

        # Parse warehouse map
        warehouse: dict = {}
        for y, row in enumerate(warehouse_map.split('\n')):
            for x, object in enumerate(row):
                warehouse[(x, y)] = object
    
        # Clean up robot movements
        motions = motions.replace('\n', '')

        return warehouse, motions
    
    def _invert_warehouse(self) -> dict:
        inverted = defaultdict(set)
        for key, value in self.warehouse.items():
            inverted[value].add(key)
        return dict(inverted)

    def _display_warehouse(self):
        for y in range(*self.limits['y']):
            row = ''
            for x in range(*self.limits['x']):
                row += self.warehouse[(x, y)]
            print(row)

    @staticmethod
    def _vector_add(x: tuple, y: tuple, magnitude: int = 1) -> tuple:
        y = map(math.prod, zip(y, (magnitude, magnitude)))
        return tuple(map(sum, zip(x, y)))

    def _process_motions(self, debug: bool = False) -> int:
        if debug:
            print(f"Initial state:")
            self._display_warehouse()

        loc_robot = list(self._invert_warehouse()['@'])[0]

        for motion in self.motions:
            loc_old = loc_robot
            loc_new = self._vector_add(loc_robot, self.directions[motion])
            if debug:
                print(f"Considering {motion} move {loc_old} to {loc_new}")

            # Verify movement is legit
            new_space = self.warehouse[loc_new]
            if debug:
                print(f"New space contains {new_space}")
            if new_space == '#':
                # Can't move through walls
                if debug:
                    print(f"Cannot move @ as {loc_new=} is a wall")
            elif new_space == 'O':
                # Boxes also move, if they can
                # To check, we need to look behind all boxes in a row until we hit a non-box
                behind_box = loc_new
                magnitude = 1
                while self.warehouse[behind_box] == 'O':
                    behind_box = self._vector_add(loc_new, self.directions[motion], magnitude)
                    magnitude += 1
                space_behind_box = self.warehouse[behind_box]
                if space_behind_box == '.':
                    # If O*.: move robot to new_loc and change behind_box to O
                    loc_robot = loc_new
                    self.warehouse[loc_new] = '@'
                    self.warehouse[loc_old] = '.'
                    self.warehouse[behind_box] = 'O'
                elif space_behind_box == '#':
                    # If O*#: don't move
                    if debug:
                        print(f"Box cannot be moved as {behind_box} is {space_behind_box}")
                else:
                    print(f"Unexpected condition {space_behind_box=}")
                    breakpoint()
            elif new_space == '.':
                # Empty spaces are a simple move
                loc_robot = loc_new
                self.warehouse[loc_new] = '@'
                self.warehouse[loc_old] = '.'
                if debug:
                    print(f"Moved @ from {loc_old=} to {loc_new=}")
            else:
                print(f"Unexpected context: {loc_robot=} {loc_old=} {loc_new=} {motion=} {new_space=}")
                breakpoint()

            if debug:
                self._display_warehouse()
                input()
    
    def solve(self) -> int:
        self._process_motions()

        # Sum of all box coords
        loc_boxes = list(self._invert_warehouse()['O'])

        total = 0
        for box_x, box_y in loc_boxes:
            total += box_x + (100 * box_y)

        return total


# RobotWarehouse("./test.txt")._display_warehouse()
# RobotWarehouse("./test.txt")._process_motions(debug=True)
assert RobotWarehouse("./test.txt").solve() == 2028
assert RobotWarehouse("./test2.txt").solve() == 10092

# A: Get sum of all box co-ords
print(f"A: {RobotWarehouse('./input.txt').solve()}")
