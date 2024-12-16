#!/usr/bin/env python3

from collections import defaultdict
from typing import Optional
import math

class MazeRunner():
    costs: dict = {
        "Forward": 1,
        "Left": 1001,
        "Right": 1001,
    }
    directions: list = [
        (-1, 0), # West - ( 0, -1)
        ( 0,-1), # North - (-1,  0)
        ( 1, 0), # East - ( 0,  1)
        ( 0, 1), # South - ( 1,  0)
    ]
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
        '#': '🧱',
        '.': '⬛',
        'S': '⬜',
        'E': '🏁',
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
    }

    def __init__(self, input_file: str) -> None:
        self.maze, self.locations = self._parse_input(input_file)
        top_left = min(self.maze.keys())
        bottom_right = max(self.maze.keys())
        self.limits = {
            'x': (top_left[0], bottom_right[0]+1),
            'y': (top_left[1], bottom_right[1]+1),
        }

    def _parse_input(self, input_file: str) -> tuple[dict, dict]:
        locations = {
            "start": None,
            "end": None,
            "walkable": set(),
            "impassable": set(),
        }
        maze = {}
        for y, row in enumerate(open(input_file).readlines()):
            for x, space in enumerate(row):
                maze[(x, y)] = space
                if space == 'S':
                    locations["start"] = (x, y)
                elif space == 'E':
                    locations["end"] = (x, y)
                elif space == '.':
                    locations["walkable"].add((x, y))
                elif space == '#':
                    locations["impassable"].add((x, y))
        return maze, locations

    @staticmethod
    def _vector_add(x: tuple, y: tuple) -> tuple:
        return tuple(map(sum, zip(x, y)))

    @staticmethod
    def _vector_rotate(current: tuple, direction: str) -> tuple:
        if direction == "Left":
            return (-current[1], current[0])
        elif direction == "Right":
            return (current[1], -current[0])
        else:
            raise ValueError(f"Unknown direction {direction}")
    
    def _display_maze(self, path_steps: Optional[list] = None):
        path_dir = defaultdict(set)
        for position, direction in path_steps:
            path_dir[position].add(direction)
        path_visual: dict = {}
        for position, directions in path_dir.items():
            if len(directions) == 1:
                path_visual[position] = self.visuals[self.path_ascii[list(directions)[0]]]
            elif len(directions) == 2:
                path_visual[position] = self.visuals[self.path_ascii[tuple(sorted(directions))]]
            else:
                path_visual[position] = '🔀'


        for y in range(*self.limits['y']):
            row = ''
            for x in range(*self.limits['x']):
                if self.maze[(x, y)] == '.' and (x, y) in path_visual.keys():
                    row += path_visual[(x, y)]
                else:
                    row += self.maze[(x, y)]
            
            for ascii, emoji in self.visuals.items():
                row = row.replace(ascii, emoji)
            print(row.strip())
        
    def shortest_dijkstras(self, debug: bool = False) -> int:
        start = self.locations["start"]
        start_direction = (1, 0)

        # Distance from start
        distances = {
            (start, start_direction): 0,
        }
        
        # Path parent
        previous = defaultdict(set)

        # Set of visited nodes
        unvisited = {
            (start, start_direction)
        }

        while unvisited:
            # Set current node to a node with the lowest distance to source
            current_node = min(unvisited, key=lambda x: distances.get(x, math.inf))
            current_position, current_heading = current_node
            # current_distance = distances[current_node]
            if debug:
                print(f"Current node is now: {current_node=}")

            # Set current node as visited
            unvisited.remove(current_node)

            if current_position == self.locations["end"]:
                break

            # Consider steps forward, left, and right
            # Distances: forward = 1, left/right = 1000

            next_steps: dict = {
                "Forward": current_heading,                             # Direction unchanged
                "Left": self._vector_rotate(current_heading, "Left"),   # Direction anticlockwise
                "Right": self._vector_rotate(current_heading, "Right"), # Direction clockwise
            }

            for move_type, heading in next_steps.items():
                candidate_location = self._vector_add(current_position, heading)
                candidate_node = (candidate_location, heading)
                if debug:
                    print(f"Considering {candidate_node=} {heading=} {move_type=}")

                # If next step is a wall, it's invalid
                if self.maze[candidate_location] == '#':
                    if debug:
                        print(f"{candidate_location=} is a wall")
                    continue

                # Determine movement cost
                move_cost = self.costs[move_type]
                new_distance = distances[current_node] + move_cost

                # Update location's distance if new distance is lower
                if new_distance <= distances.get(candidate_node, math.inf):
                    distances[candidate_node] = new_distance
                    previous[candidate_node].add(current_node)
                    unvisited.add(candidate_node)
                    if debug:
                        print(f"{unvisited=}")
                
        # Catch broken paths
        if current_node[0] != self.locations["end"]:
            return math.inf, None
        else:
            distance = distances[current_node]

        # Trace paths
        next_nodes = {current_node}

        nodes_in_paths = {current_node}
        while next_nodes:
            latest_node = next_nodes.pop()
            nodes_in_paths.add(latest_node)
            for next_node in previous[latest_node]:
                next_nodes.add(next_node)

        return distance, nodes_in_paths
    
    def find_shortest_path(self, debug: bool = False) -> int:
        distance, nodes_in_paths = self.shortest_dijkstras()

        if debug:
            # Visualise maze, with path visible
            self._display_maze(nodes_in_paths)
            print()

        return distance, len(set([node[0] for node in nodes_in_paths]))

assert MazeRunner("./test.txt").find_shortest_path(debug=True) == (7036, 45)
assert MazeRunner("./test2.txt").find_shortest_path(debug=True) == (11048, 64)

solver = MazeRunner("./input.txt")
solution_a, solution_b = solver.find_shortest_path()
print(f"A: {solution_a}")  # 85480
print(f"B: {solution_b}")  # 518
