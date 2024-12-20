#!/usr/bin/env python3

from collections import Counter, defaultdict
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

    def __init__(self, input_file: str) -> None:
        self.track, self.locations = self._parse_input(input_file)
        top_left = min(self.track.keys())
        bottom_right = max(self.track.keys())
        self.limits = {
            'x': (top_left[0], bottom_right[0]+1),
            'y': (top_left[1], bottom_right[1]+1),
        }
        self.initial_time, self.full_path = self._shortest_dijkstras()
        self.cheats = self._find_cheats(self.full_path)
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

    def _display_track(self, path_steps: Optional[dict] = {}, cheat: Optional[tuple[tuple[int, int], tuple[int, int]]] = None):
        for y in range(*self.limits['y']):
            row = ''
            for x in range(*self.limits['x']):
                if cheat is not None and (x, y) == cheat[1]:
                    row += self.visuals['1']
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

    def _find_cheats(self, path_nodes: dict) -> set:
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

    def count_cheats(self, threshold: int = 100) -> int:
        cheat_times = {}
        for c_start, c_skip, c_end in self.cheats:
            # time_w_cheat, path_w_cheat = self._shortest_dijkstras(cheat=c_skip)
            # time_saved = self.initial_time - time_w_cheat
            time_saved = self.full_path[c_end] - self.full_path[c_start] - 2


            # if time_saved > 35:
            #     path_w_cheat = {
            #         position: distance
            #         for position, distance in self.full_path.items()
            #         if (distance <= self.full_path[c_start]) or (distance >= self.full_path[c_end])
            #     }
            #     self._display_track(path_steps=path_w_cheat, cheat=(c_start, c_skip, c_end))
            #     print(f"Time Saved: {time_saved}")
            #     breakpoint()
            cheat_times[(c_start, c_end)] = time_saved
        
        # counts = Counter(cheat_times)
        return len([cheat for cheat, saving in cheat_times.items() if saving >= threshold])
        
# print(RaceTrack("./test.txt").count_cheats())

print(f"A: {RaceTrack('./input.txt').count_cheats()}")
