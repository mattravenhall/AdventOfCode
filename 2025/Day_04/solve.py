#!/usr/bin/env python3

neighbours = (
        (-1, -1), (0, -1), (1, -1),
        (-1,  0),          (1,  0),
        (-1,  1), (0,  1), (1,  1),
)


def _is_valid(roll: tuple[int, int], rolls: set[tuple[int, int]]) -> bool:
    n_rolls = 0
    for neighbour in neighbours:
        candidate = tuple(map(sum, zip(roll, neighbour)))
        n_rolls += int(candidate in rolls)
    return n_rolls < 4
    

def solve(lines: list[str]) -> int:
    floor = {}
    empty = set() 
    rolls = set() 
    
    # Load floor
    for y, line in enumerate(lines):
        for x, tile in enumerate(line.strip()):
            pos = (x, y)
            floor[pos] = tile
            match tile:
                case '.':
                    empty.add(pos)
                case '@':
                    rolls.add(pos)
                case _:
                    raise ValueError(f"Unknown tile type: {tile}")
    
    # A: Counts rolls with fewer than four neighbouring rolls
    valid_rolls = 0
    for roll in rolls:
        valid_rolls += int(_is_valid(roll, rolls))

    # B: How many rolls can be removed, if we keep removing removable rolls?
    removable_rolls = 0
    searching = True
    while searching:
        removable = set()
        for roll in rolls:
            if _is_valid(roll, rolls):
                removable.add(roll)
        
        # Keep searching until we find nothing more to remove
        searching = bool(removable)
        removable_rolls += len(removable)
        rolls -= removable

    return valid_rolls, removable_rolls

assert solve(open("test.txt").readlines()) == (13, 43)

print(solve(open('input.txt').readlines()))


