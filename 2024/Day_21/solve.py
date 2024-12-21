#!/usr/bin/env python3

from functools import cache
import re


class Pad:
    name: str
    position: tuple
    positions: dict
    directions: dict = {
        '<': (-1,  0),
        '>': ( 1,  0),
        '^': ( 0, -1),
        'V': ( 0,  1),
    }
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.reset()

    @staticmethod
    @cache
    def _vector_add(x: tuple, y: tuple) -> tuple:
        return tuple(map(sum, zip(x, y)))
        
    def reset(self):
        self.position = self.positions['A']

    @cache
    def _in_bounds(self, position: tuple) -> bool:
        on_grid = position in self.positions.values()
        is_void = self.positions['X'] == position
        return on_grid and not is_void

    @cache
    def _path_is_valid(self, start: tuple, path: tuple) -> bool:
        if self.positions_inv[start] == 'X':
            return False
        pos = start
        for move in path:
            pos = self._vector_add(pos, self.directions[move])
            if self.positions_inv[pos] == 'X':
                return False
        return True

    @cache
    def _find_path_to(self, position: tuple, destination: str) -> str:
        """Identify the shortest path to a given location from the current position, return the movement sequence"""

        position_orig = position
        if destination not in self.positions:
            raise ValueError
        
        coords_dest = self.positions[destination]

        # Step towards destination one-by-one
        path = ''
        while position != coords_dest:
            d_x = coords_dest[0] - position[0]
            d_y = coords_dest[1] - position[1]
            
            if d_x:
                delta = 1 if d_x > 0 else -1
                candidate = self._vector_add(position, (delta, 0))
                if self._in_bounds(candidate):
                    position = candidate
                    path += '<' if delta < 0 else '>'
                    continue
            if d_y:
                delta = 1 if d_y > 0 else -1
                candidate = self._vector_add(position, (0, delta))
                if self._in_bounds(candidate):
                    position = candidate
                    path += '^' if delta < 0 else 'V'
                    continue

        # Sort path with <^V> priority, if it's invalid just use the reverse
        path_sorted = ''.join(sorted(path, key=lambda x: ['<^V>'.index(y) for y in x]))
        if not self._path_is_valid(position_orig, path_sorted):
            path_sorted = path_sorted[::-1]
        path = path_sorted + 'A'

        return path


class DigitPad(Pad):
    positions: dict = {
        '7': (0, 0),
        '8': (1, 0),
        '9': (2, 0),
        '4': (0, 1),
        '5': (1, 1),
        '6': (2, 1),
        '1': (0, 2),
        '2': (1, 2),
        '3': (2, 2),
        'X': (0, 3),
        '0': (1, 3),
        'A': (2, 3),
    }
    positions_inv = {v: k for k, v in positions.items()}

    def __init__(self, name: str):
        super().__init__(name)


class ArrowPad(Pad):
    positions: dict = {
        'X': (0, 0),
        '^': (1, 0),
        'A': (2, 0),
        '<': (0, 1),
        'V': (1, 1),
        '>': (2, 1),
    }
    positions_inv = {v: k for k, v in positions.items()}

    def __init__(self, name: str):
        super().__init__(name)


class ButtonChain:
    def __init__(self, input_file: str, dir_robots: int = 2) -> None:
        self.input_codes = self._parse_input(input_file)
        self.pads = [
            DigitPad(name="Digit0"),
        ]
        for i in range(dir_robots):
            self.pads.append(ArrowPad(name=f"Arrow{i}"))
    
    def _parse_input(self, input_file: str) -> tuple[dict, dict]:
        return open(input_file).read().strip().split('\n')
    
    @cache
    def _find_shortest_sequence(self, code: str) -> str:
        for pad in self.pads:
            sequence = ''
            for destination in code:
                sequence += pad._find_path_to(pad.position, destination)
                pad.position = pad.positions[destination]
            code = sequence
        return code

    def reset(self):
        """Reset locations of all pad robots"""
        for pad in self.pads:
            pad.reset()

    def calc_complexities(self) -> int:
        total_complexity = 0
        for input_code in self.input_codes:
            len_seq = len(self._find_shortest_sequence(input_code))
            num_code = int(re.match(r'\d+', input_code).group())
            complexity = len_seq * num_code
            total_complexity += complexity
        return total_complexity


# Ensure path finding works as expected
# path_tester = ButtonChain("./test.txt")
# assert len(path_tester.pads[0]._find_path_to('1')) == 4
# assert path_tester.pads[0]._find_path_to('1') == "A"
# path_tester.pads[0].reset()
# assert len(path_tester.pads[0]._find_path_to('8')) == 5

# assert len(path_tester.pads[1]._find_path_to('<')) == 4
# assert path_tester.pads[1]._find_path_to('<') == 'A'
# path_tester.pads[1].reset()
# assert path_tester.pads[1]._find_path_to('>') == 'VA'

tester = ButtonChain("./test.txt")
assert len(tester._find_shortest_sequence("029A")) == 68
assert len(tester._find_shortest_sequence("980A")) == 60
assert len(tester._find_shortest_sequence("179A")) == 68
assert len(tester._find_shortest_sequence("456A")) == 64
assert len(tester._find_shortest_sequence("379A")) == 64
assert ButtonChain("./test.txt").calc_complexities() == 126384

print(f"A: {ButtonChain('./input.txt', dir_robots=2).calc_complexities()}")
print(f"B: {ButtonChain('./input.txt', dir_robots=25).calc_complexities()}")

