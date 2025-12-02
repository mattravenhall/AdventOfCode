#!/usr/bin/env python3

def solve(filepath: str, debug: bool = False) -> tuple[int, int]:
    position = 50
    zero_landings = 0
    zero_passes = 0
    
    for command in open(filepath).readlines():
        # Pass commands
        direction = command[0]
        magnitude = int(command.strip()[1:])
        travel = magnitude * (int(direction == 'R') * 2 - 1)

        # Update positions
        position_old = position
        position_new = position + travel
        position = position_new % 100
       
        # Determine remainder of rotations for later removal
        if direction == 'R':
            distance_from_edge = (100 - position_old) % 100
        else:
            distance_from_edge = position_old % 100
        if distance_from_edge == 0:
            distance_from_edge = 100

        # Update passwords
        zero_landings += int(position == 0)
        zero_passes += 1 + (magnitude - distance_from_edge) // 100

    return zero_landings, zero_passes

test_a, test_b = solve("test.txt", debug=True)
assert test_a == 3
assert test_b == 6

solution_a, solution_b = solve("input.txt")
print(f"{solution_a=}")
print(f"{solution_b=}")
