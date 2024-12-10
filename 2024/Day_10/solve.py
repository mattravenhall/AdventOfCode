#!/usr/bin/env python3

class TrailFinder():
    directions = [
        (-1,  0), # Up
        ( 0, -1), # Left
        ( 0,  1), # Right
        ( 1,  0), # Down
    ]

    def __init__(self, input_path: str):
        self.grid, self.trailheads = self._parse_input(input_path)
        
    def _not_in_range(self, x: int, y: int):
        return x not in range(0, len(self.grid)) or y not in range(0, len(self.grid[0]))

    def _parse_input(self, input_path: str) -> tuple[list[list[str]], set]:
        grid = []
        trailheads = set()
        for i, line in enumerate(open(input_path).readlines()):
            line = line.strip()
            if not line:
                continue
            grid.append(line)

            for j, pos in enumerate(line):
                if pos == '0':
                    trailheads.add((i, j))
        
        # print([grid[x][y] for x, y in trailheads])
        return grid, trailheads

    def _find_peaks(self, position: tuple[int, int]) -> tuple[set[tuple[int, int]], int]:
        # Start at trailhead, recursively search for 9 - if found, return it
        x, y = position
        height = self.grid[x][y]

        # If out of range, this path isn't valid
        if self._not_in_range(x, y):
            return set(), 0

        # If current height is '9', return 1 all the way up
        if height == '9':
            return {position}, 1

        # For each direction
        peaks = set()
        trail_count = 0
        for direction in self.directions:
            next_x, next_y = tuple(map(sum, zip(position, direction)))

            # If out of range, this path isn't valid
            if self._not_in_range(next_x, next_y) or not self.grid[next_x][next_y].isdigit():
                continue

            # If value is +1 of current height
            if int(height) == int(self.grid[next_x][next_y]) - 1:
                found_peaks, found_trails = self._find_peaks((next_x, next_y))
                peaks = peaks.union(found_peaks)
                trail_count += found_trails

        return peaks, trail_count

    def solve(self) -> tuple[int, int]:
        peak_counts = 0
        trail_counts = 0
        for trailhead in self.trailheads:
            found_peaks, found_trails = self._find_peaks(trailhead)
            peak_counts += len(found_peaks)
            trail_counts += found_trails
        return peak_counts, trail_counts

    def solve_b(self) -> int:
        pass


assert TrailFinder("./test.txt").solve() == (36, 81)
assert TrailFinder("./test2.txt").solve() == (2, 2)
assert TrailFinder("./test3.txt").solve() == (4, 13)

finder = TrailFinder("./input.txt")
solution_a, solution_b = finder.solve()

print(f"A: {solution_a}")
print(f"B: {solution_b}")
