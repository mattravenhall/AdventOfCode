#!/usr/bin/env python3

from collections import defaultdict
from functools import cache, partial


class GardenExplorer():
    directions: list[tuple[int, int]] = [
        ( 0, -1), # Left
        (-1,  0), # Up
        ( 0,  1), # Right
        ( 1,  0), # Down
    ]

    def __init__(self, input_file: str) -> None:
        self.map = self._parse_input(input_file)

    def _parse_input(self, input_file: str) -> list[str]:
        parsed_map: list[str] = []
        for line in open(input_file).readlines():
            parsed_map.append(line.strip())
        return parsed_map

    @staticmethod
    def _vector_add(x: tuple, y: tuple) -> tuple:
        return tuple(map(sum, zip(x, y)))
    
    def _out_of_range(self, x, y) -> bool:
        if x < 0 or y < 0 or x >= len(self.map) or y >= len(self.map[0]):
            return True
        else:
            return False

    def _explore_garden(self, x: int, y: int, owner: str, spaces=None) -> dict:
        if spaces is None:
            spaces = defaultdict(set)

        # Scout around
        candidates = set()
        for direction in self.directions:
            new_x, new_y = self._vector_add((x, y), direction)

            if self._out_of_range(new_x, new_y) or self.map[new_x][new_y] != owner:
                # Border found, update accordingly
                spaces[(x, y)].add((new_x, new_y))
                continue
            elif (new_x, new_y) in spaces.keys():
                # Already been here
                continue
            else:
                candidates.add((new_x, new_y))
                spaces[(new_x, new_y)] = set()
        
        # Step into same regions
        for new_x, new_y in candidates:
            spaces |= self._explore_garden(new_x, new_y, owner, spaces)
        
        return spaces

    @staticmethod
    @cache
    def _x_neighbour(inside: tuple[int, int], outside: tuple[int, int], distance: int) -> tuple:
        i_x, i_y = inside
        o_x, o_y = outside
        return ((i_x+distance, i_y), (o_x+distance, o_y))

    @staticmethod
    @cache
    def _y_neighbour(inside: tuple[int, int], outside: tuple[int, int], distance: int) -> tuple:
        i_x, i_y = inside
        o_x, o_y = outside
        return ((i_x, i_y+distance), (o_x, o_y+distance))

    def _count_sides(self, garden: dict) -> int:
        # Borders are inside:outside coordinate pairs
        borders = set()
        for key, values in garden.items():
            for value in values:
                borders.add(tuple([key, value]))

        sides = set()
        while borders:
            inside, outside = borders.pop()
            side = {(inside, outside)}
            print(f"origin={inside}, {outside}")

            # Travel on x axis
            distance = 1
            x_neighbour = partial(self._x_neighbour, inside, outside)
            y_neighbour = partial(self._y_neighbour, inside, outside)

            if {x_neighbour(-distance), x_neighbour(distance)} & borders:
                # Travel down
                while x_neighbour(distance) in borders:
                    borders -= {x_neighbour(distance)}
                    side.add(x_neighbour(distance))
                    distance += 1

                # Travel up
                distance = -1
                while x_neighbour(distance) in borders:
                    borders -= {x_neighbour(distance)}
                    side.add(x_neighbour(distance))
                    distance -= 1

            elif {y_neighbour(-distance), y_neighbour(distance)} & borders:
                # Travel right
                while y_neighbour(distance) in borders:
                    borders -= {y_neighbour(distance)}
                    side.add(y_neighbour(distance))
                    distance += 1

                # Travel left
                distance = -1
                while y_neighbour(distance) in borders:
                    borders -= {y_neighbour(distance)}
                    side.add(y_neighbour(distance))
                    distance -= 1
            else:
                # Side of length one
                pass
            
            sides.add(tuple(sorted(side)))
        # breakpoint()
        return len(sides)

    def calculate_fence_cost(self, apply_discount: bool = False):
        # Find gardens
        visited: set = set()
        gardens: list[dict] = []
        for x, row in enumerate(self.map):
            for y, _col in enumerate(row):
                # Don't revisit a space
                if (x, y) in visited:
                    continue
            
                garden = self._explore_garden(x, y, self.map[x][y])
                gardens.append(garden)
                visited |= garden.keys()
        
        # Calculate costs
        total: int = 0
        for garden in gardens:
            area = len(garden)
            if apply_discount:
                n_sides = self._count_sides(garden)
                print(f"{area=} * {n_sides=}")
                total += area * n_sides
            else:
                perimeter = sum([len(borders) for borders in garden.values()])
                total += area * perimeter
        print(total)

        return total


assert GardenExplorer("./test.txt").calculate_fence_cost() == 1930
assert GardenExplorer("./test.txt").calculate_fence_cost(apply_discount=True) == 1206
assert GardenExplorer("./test2.txt").calculate_fence_cost() == 772
assert GardenExplorer("./test3.txt").calculate_fence_cost(apply_discount=True) == 80
assert GardenExplorer("./test4.txt").calculate_fence_cost(apply_discount=True) == 236
assert GardenExplorer("./test5.txt").calculate_fence_cost(apply_discount=True) == 368
assert GardenExplorer("./test6.txt").calculate_fence_cost(apply_discount=True) == 138
assert GardenExplorer("./test7.txt").calculate_fence_cost(apply_discount=True) == 138

solver = GardenExplorer("./input.txt")
print(f"A: {solver.calculate_fence_cost()}")  # 1452678
print(f"B: {solver.calculate_fence_cost(apply_discount=True)}")  # 852753

