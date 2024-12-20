#!/usr/bin/env python3

from collections import defaultdict
import math
import random
from typing import Optional


class RaceTrack:
    directions: list = {
        "Left": (-1, 0), # Left
        "Up": ( 0,-1), # Up
        "Right": ( 1, 0), # Right
        "Down": ( 0, 1), # Down
    }
    path_ascii: dict = {
        (-1, 0): '<', # West
        ( 0,-1): '^', # North
        ( 1, 0): '>', # East
        ( 0, 1): 'v', # South
        (( 0,-1), ( 1, 0)):  '┐',
        (( 0, 1), ( 1, 0)): '┘',
        ((-1, 0), ( 0, 1)): 'L',
        ((-1, 0), ( 0,-1)): '┌',
        (( 0,-1), ( 0, 1)): '║',
        ((-1, 0), ( 1, 0)): '═',
    }
    visuals: dict = {
        'X': '🎄',
        # '#': '🟩',
        '.': '⬛',
        'S': '🚩',
        'E': '🏁',
        'P': '🏾', #'🟨',
        '1': '🔷',
        '+': '🟪',
        '2': '🔶',
        '<': '⬅️ ',
        '^': '⬆️ ',
        '>': '➡️ ',
        'v': '⬇️ ',
        'x': '🔀',
        '┐': '↗️ ',
        '┘': '↘️ ',
        'L': '↙️ ',
        '┌': '↖️ ',
        '║': '↕️ ',
        '═': '↔️ ',
        '*': '🪶',
    }

    def __init__(self, input_file: str, debug: bool = False) -> None:
        self.track, self.locations = self._parse_input(input_file)
        top_left = min(self.track.keys())
        bottom_right = max(self.track.keys())
        self.limits = {
            'x': (top_left[0], bottom_right[0]+1),
            'y': (top_left[1], bottom_right[1]+1),
        }
        self.initial_time, self.full_path = self._shortest_dijkstras()
        if debug:
            self._display_track(path_steps=self.full_path)

    def _parse_input(self, input_file: str) -> tuple[dict, dict]:
        locations = {
            "start": None,
            "end": None,
            "walkable": set(),
            "impassable": set(),
        }
        track = {}
        for y, row in enumerate(open(input_file).readlines()):
            row = row.strip()
            for x, space in enumerate(row):
                track[(x, y)] = space
                if space == 'S':
                    locations["start"] = (x, y)
                elif space == 'E':
                    locations["end"] = (x, y)
                elif space == '.':
                    locations["walkable"].add((x, y))
                elif space == '#':
                    locations["impassable"].add((x, y))
        return track, locations

    @staticmethod
    def _vector_add(x: tuple, y: tuple) -> tuple:
        return tuple(map(sum, zip(x, y)))

    def _on_border(self, position: tuple) -> bool:
        if position[0] == self.limits['x'][0]:
            return True
        if position[0] == self.limits['x'][1]-1:
            return True
        if position[1] == self.limits['y'][0]:
            return True
        if position[1] == self.limits['y'][1]-1:
            return True
        return False

    def _display_track(self, path_steps: Optional[dict] = {}, cheat: Optional[tuple[tuple, tuple, tuple]] = None):
        for y in range(*self.limits['y']):
            row = ''
            for x in range(*self.limits['x']):
                if cheat is not None and (x, y) == cheat[0]:
                    row += self.visuals['1']
                elif cheat is not None and (x, y) == cheat[1]:
                    row += self.visuals['+']
                elif cheat is not None and (x, y) == cheat[2]:
                    row += self.visuals['2']
                elif self._on_border((x, y)):
                    row += self.visuals['X']
                elif self.track[(x, y)] == '.':
                    if (x, y) in path_steps.keys():
                        row += self.visuals['P']
                    else:
                        row += self.visuals['.']
                elif self.track[(x, y)] in {'S','E'}:
                    row += self.track[(x, y)]                    
                else:
                    row += random.choice("🌳🌲🎄")
            
            for ascii, emoji in self.visuals.items():
                row = row.replace(ascii, emoji)
            print(row.strip())

    def _shortest_dijkstras(self, cheat: Optional[tuple[int, int]] = None) -> tuple[int, dict]:
        start = self.locations["start"]

        # Distance from start
        distances = {
            start: 0,
        }
        
        # Path parent
        previous = defaultdict(set)

        # Set of visited nodes
        unvisited = {
            start
        }

        while unvisited:
            # Set current node to a node with the lowest distance to source
            current_position = min(unvisited, key=lambda x: distances.get(x, math.inf))

            # Set current node as visited
            unvisited.remove(current_position)

            # Break when hitting the end
            if current_position == self.locations["end"]:
                break

            # Consider up, down, left, and right
            next_steps: dict = {
                direction: self._vector_add(current_position, self.directions[direction])
                for direction in self.directions.keys()
            }
            for _, candidate_location in next_steps.items():

                # If next step is a wall, it's invalid
                if candidate_location != cheat:
                    if self.track[candidate_location] in {'#', 'X'}:
                        continue

                # Determine movement cost
                new_distance = distances[current_position] + 1

                # Update location's distance if new distance is lower
                if new_distance <= distances.get(candidate_location, math.inf):
                    distances[candidate_location] = new_distance
                    previous[candidate_location].add(current_position)
                    unvisited.add(candidate_location)
                
        # Catch broken paths
        if current_position != self.locations["end"]:
            return math.inf, None
        else:
            distance = distances[current_position]

        # Trace paths
        next_nodes = {current_position}

        nodes_in_paths = {current_position: distance}
        while next_nodes:
            latest_node = next_nodes.pop()
            nodes_in_paths[latest_node] = distances[latest_node]
            for next_node in previous[latest_node]:
                next_nodes.add(next_node)

        return distance, nodes_in_paths

    def _get_path_in_manhattan_distance(self, origin: tuple, max_distance: int = 20) -> set:
        """Identify candidate skip locations within a maximum manhattan distance"""
        coords = set()
        for dx in range(-max_distance, max_distance + 1):
            dist_remaining = max_distance - abs(dx)
            for dy in range(-dist_remaining, dist_remaining + 1):
                # Don't include self
                if dx == 0 and dy == 0:
                    continue

                cand_x = origin[0] + dx
                cand_y = origin[1] + dy
                candidate = (cand_x, cand_y)

                # Don't include out of bound
                if not (self.limits['x'][0] <= cand_x <= self.limits['x'][1]):
                    continue
                if not (self.limits['y'][0] <= cand_y <= self.limits['y'][1]):
                    continue
                
                # Only include paths and exits
                if candidate not in self.full_path.keys():
                    continue

                # Don't include upstream exits
                if self.full_path[candidate] < self.full_path[origin]:
                    continue

                # Don't include paths that aren't shortcuts
                distance = max_distance - (dist_remaining - abs(dy))
                if distance == 0:
                    continue
                if (self.full_path[candidate] - self.full_path[origin]) <= distance:
                    continue

                coords.add(((cand_x, cand_y), distance))
        return coords
    
    @staticmethod
    def manhattan_distance(x: tuple, y: tuple) -> int:
        return abs(x[0] - y[0]) + abs(x[1] - y[1])
    
    def _find_cheats_part_1(self, path_nodes: dict) -> set:
        """Travel path and locate cheat locations ('#' with '.' behind)"""
        cheats = set()
        for cheat_enter in path_nodes.keys():
            for _, direction in self.directions.items():
                # Cheat skip must be impassable
                cheat_skip = self._vector_add(cheat_enter, direction)
                if self.track[cheat_skip] != '#' or self._on_border(cheat_skip):
                    continue
                cheat_exit = self._vector_add(cheat_skip, direction)

                # Cheat exit must be on the path at a larger distance
                if self.track[cheat_exit] in {'.', 'E'}:
                    if path_nodes[cheat_exit] > path_nodes[cheat_enter]:
                        cheats.add((cheat_enter, cheat_skip, cheat_exit))
        return cheats
    
    def _find_cheats_part_2(self, path_nodes: dict) -> set:
        """Just scan around with a distance of X, find spaces that reduce distance taken, return no cheat_skip"""
        cheats = set()
        for cheat_enter in path_nodes.keys():
            for cheat_exit, distance in self._get_path_in_manhattan_distance(cheat_enter):
                # Cheat exit must be on the path at a larger distance
                if path_nodes[cheat_exit] > path_nodes[cheat_enter]:
                    cheats.add((cheat_enter, '', cheat_exit))
        return cheats

    def count_cheats(self, part: int, threshold: int = 100, debug: bool = False) -> int:
        """Determine time saved by each cheat, count up the number that exceed our threshold"""
        if part == 1:
            self.cheats = self._find_cheats_part_1(self.full_path)
        else:
            self.cheats = self._find_cheats_part_2(self.full_path)

        cheat_times = {}
        for c_enter, c_skip, c_exit in self.cheats:
            time_saved = self.full_path[c_exit] - self.full_path[c_enter] - self.manhattan_distance(c_enter, c_exit)

            if time_saved:
                if debug:
                    path_w_cheat = {
                        position: distance
                        for position, distance in self.full_path.items()
                        if (distance <= self.full_path[c_enter]) or (distance >= self.full_path[c_exit])
                    }
                    self._display_track(path_steps=path_w_cheat, cheat=(c_enter, c_skip, c_exit))
                    print(f"Time Saved: {time_saved}")
                    breakpoint()
                if part == 1:
                    c_skip = '|'.join(map(str,c_skip))
                cheat_times[(c_enter, c_skip, c_exit)] = time_saved

        return len([cheat for cheat, saving in cheat_times.items() if saving >= threshold])

assert RaceTrack("./test.txt", debug=False).count_cheats(part=1, threshold=0) == 44
assert RaceTrack("./test.txt", debug=False).count_cheats(part=2, threshold=50) == 285

print(f"A: {RaceTrack('./input.txt', debug=False).count_cheats(part=1)}")  # 1367
print(f"B: {RaceTrack('./input.txt', debug=False).count_cheats(part=2)}")  # 1006850
