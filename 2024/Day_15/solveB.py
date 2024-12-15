#!/usr/bin/env python3

from collections import defaultdict
import math


class BigRobotWarehouse():
    directions = {
        '>': (1, 0),
        '<': (-1, 0),
        '^': (0, -1),
        'v': (0, 1),
    }
    tiles = {
        '#': "##",
        'O': "[]",
        '.': "..",
        '@': "@.",
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
                warehouse[((x*2)-1, y)] = self.tiles[object][0]
                warehouse[(x*2, y)] = self.tiles[object][1]
    
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

    def _find_full_box(self, loc: tuple[int, int]) -> list[tuple[int, int]]:
        if self.warehouse[loc] == '[':
            return [loc, (loc[0]+1, loc[1])]
        elif self.warehouse[loc] == ']':
            return [loc, (loc[0]-1, loc[1])]

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
            elif new_space in '[]':
                # Boxes also move, if they can
                # To check, we need to look behind all boxes in a row until we hit a non-box
                if motion in '<>':
                    # Left-right movement is essentially unchanged
                    behind_box = loc_new
                    magnitude = 1
                    loc_boxes = []
                    while self.warehouse[behind_box] in '[]':
                        loc_boxes.append(behind_box)
                        behind_box = self._vector_add(loc_new, self.directions[motion], magnitude)
                        magnitude += 1
                    space_behind_box = self.warehouse[behind_box]
                    if space_behind_box == '.':
                        # If []*.: move robot to new_loc and shuffle boxes
                        loc_robot = loc_new

                        # Shuffle boxes
                        if motion == '<':
                            self.warehouse[behind_box] = '['
                        elif motion == '>':
                            self.warehouse[behind_box] = ']'
                        else:
                            raise Exception(f"Unexpected motion {motion}")
                        
                        for loc_box in loc_boxes:
                            if self.warehouse[loc_box] == '[':
                                self.warehouse[loc_box] = ']'
                            elif self.warehouse[loc_box] == ']':
                                self.warehouse[loc_box] = '['

                        # Move robot last
                        self.warehouse[loc_new] = '@'
                        self.warehouse[loc_old] = '.'
                    elif space_behind_box == '#':
                        # If []*#: don't move
                        if debug:
                            print(f"Box cannot be moved as {behind_box} is {space_behind_box}")
                    else:
                        print(f"Unexpected condition {space_behind_box=}")
                        breakpoint()
                elif motion in '^v':
                    # When moving up or down, boxes can branch
                    boxes_to_move = []

                    # Create initial search layer
                    boxes_in_next_layer: set = set(self._find_full_box(loc_new))

                    # Check if boxes can be moved, collect boxes as we go
                    can_be_moved = None
                    while can_be_moved is None:
                        # Shift to next search layer
                        boxes_in_layer = boxes_in_next_layer
                        boxes_in_next_layer = set()
                        if debug:
                            print(f"Investigating layer: {boxes_in_layer}")
                            input()

                        # Check behind each box in layer
                        objects_behind_boxes: set = set()
                        for box in boxes_in_layer:
                            behind_box = self._vector_add(box, self.directions[motion], 1)
                            object_behind_box = self.warehouse[behind_box]

                            objects_behind_boxes.add(object_behind_box)
                            if object_behind_box == '#':
                                can_be_moved = False
                                break
                            elif object_behind_box in "[]":
                                # Add both box halves to boxes_in_next_layer
                                boxes_in_next_layer |= set(self._find_full_box(behind_box))
                            elif object_behind_box == '.':
                                # Add this box to boxes to move
                                pass
                            else:
                                print(f"Unexpected space found {object_behind_box}")
                                breakpoint()                        
                        boxes_to_move.extend(boxes_in_layer)

                        # If all boxes are '.', we can start moving boxes
                        if objects_behind_boxes == {'.'}:
                            can_be_moved = True
                    
                    if can_be_moved:
                        # Always start at the end of the push
                        if motion == '^':
                            sorted_boxes = sorted(boxes_to_move)
                        elif motion == 'v':
                            sorted_boxes = sorted(boxes_to_move)[::-1]
                        else:
                            raise Exception(f"Unexpected motion {motion}")

                        # Actually move stuff
                        for box in sorted_boxes:
                            
                            new_loc = self._vector_add(box, self.directions[motion])
                            self.warehouse[new_loc] = self.warehouse[box]
                            self.warehouse[box] = '.'

                            if debug:
                                print(f"Moved {box} to {new_loc}")
                                print(f"{sorted_boxes=}")
                                self._display_warehouse()
                                input()

                        # Move robot
                        self.warehouse[loc_new] = '@'
                        self.warehouse[loc_robot] = '.'
                        loc_robot = loc_new
                    else:
                        # Cannot be moved, so just continue
                        continue
                else:
                    print(f"Unexpected motion {motion}")
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
        loc_boxes = list(self._invert_warehouse()['['])

        total = 0
        for box_x, box_y in sorted(loc_boxes):
            total += (box_x + 1) + (100 * box_y)

        # self._display_warehouse()
        # print(total)
        return total


# BigRobotWarehouse("./test3.txt")._display_warehouse()
# BigRobotWarehouse("./test.txt")._process_motions(debug=True)
# BigRobotWarehouse("./test2.txt")._process_motions(debug=True)
# BigRobotWarehouse("./test3.txt")._process_motions(debug=True)
# BigRobotWarehouse("./test4.txt")._process_motions(debug=True)
assert BigRobotWarehouse("./test2.txt").solve() == 9021

# B: Get sum of all box co-ords, where x is twice as big
print(f"B: {BigRobotWarehouse('./input.txt').solve()}")
