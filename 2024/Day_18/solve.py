#!/usr/bin/env python3

from collections import defaultdict
import logging
import math
from typing import Optional


logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


class PathFinder:
    directions = [
        ( 0, -1),  # Up
        ( 0,  1),  # Down
        (-1,  0),  # Left
        ( 1,  0),  # Right
    ]
    visuals: dict = {
        '#': '🕳️ ',
        'x': '🟪',
        '.': '🟩',
        "start": '⬜',
        "path": '🔲',
        "end": '🏁',
    }

    def __init__(self, input_file: str, memory_space: tuple[int, int] = (0, 71)) -> None:
        self.incoming_bytes = self._parse_input(input_file)
        self.limits = {
            'x': (memory_space[0], memory_space[1]),
            'y': (memory_space[0], memory_space[1]),
        }
        self.locations = {
            "start": (self.limits['x'][0], self.limits['y'][0]),
            "end": (self.limits['x'][1]-1, self.limits['y'][1]-1),
        }
    
    def _parse_input(self, input_file: str) -> dict[tuple[int, int], int]:
        incoming_bytes = {
            tuple(map(int, position.strip().split(','))): i
            for i, position in enumerate(open(input_file).readlines())
        }
        return incoming_bytes

    @staticmethod
    def _vector_add(x: tuple, y: tuple) -> tuple:
        return tuple(map(sum, zip(x, y)))

    def _out_of_bounds(self, position: tuple) -> bool:
        if not (self.limits['x'][0] <= position[0] < self.limits['x'][1]):
            return True
        if not (self.limits['y'][0] <= position[1] < self.limits['y'][1]):
            return True
        return False

    def _display_space(self, n_bytes: int = None, path_nodes: set = set()):
        if n_bytes is None:
            n_bytes = len(self.incoming_bytes)

        for y in range(*self.limits['y']):
            row = ''
            for x in range(*self.limits['x']):
                if 0 <= self.incoming_bytes.get((x, y), -1) <= n_bytes:
                    row += self.visuals['#']
                elif (x, y) == self.locations["start"]:
                    row += self.visuals["start"]
                elif (x, y) == self.locations["end"]:
                    row += self.visuals["end"]
                elif (x, y) in path_nodes:
                    row += self.visuals["path"]
                else:
                    row += self.visuals['.']
            print(row.strip())

    def shortest_dijkstras(self, n_bytes: Optional[int] = None, visuals: bool = True) -> int:
        if n_bytes is None:
            n_bytes = len(self.incoming_bytes)
        
        if visuals:
            logger.info("> Initial State")
            self._display_space(n_bytes=n_bytes)
        
        start = self.locations["start"]

        # Distance from start
        distances = {
            start: 0,  # TODO: May need to revisit this? Distance may be dynamic if bytes are added per step?
        }
        
        # Path parent
        previous = defaultdict(set)

        # Set of visited nodes
        unvisited = {
            start,
        }

        while unvisited:
            # Set current node to a node with the lowest distance to source
            current_position = min(unvisited, key=lambda x: distances.get(x, math.inf))
            logger.debug(f"Current position is now: {current_position=}")

            # Set current node as visited
            unvisited.remove(current_position)

            # Solved
            if current_position == self.locations["end"]:
                break

            # Consider each non-diagonal neighbours
            for direction in self.directions:
                candidate_location = self._vector_add(current_position, direction)
                logger.debug(f"Considering {candidate_location=} {direction=}")
                    
                # If next step is out of bounds, it's invalid
                if self._out_of_bounds(candidate_location):
                    logger.debug(f"{candidate_location=} is out of bounds")
                    continue

                # If next step is missing, it's invalid
                if self.incoming_bytes.get(candidate_location, math.inf) <= n_bytes:
                    logger.debug(f"{candidate_location=} is missing")
                    continue

                # Determine movement cost
                new_distance = distances[current_position] + 1

                # Update location's distance if new distance is lower
                if new_distance <= distances.get(candidate_location, math.inf):
                    distances[candidate_location] = new_distance
                    previous[candidate_location].add(current_position)
                    unvisited.add(candidate_location)
                    logger.debug(f"{unvisited=}")
        
        # Catch broken paths
        if current_position != self.locations["end"]:
            return math.inf, None
        else:
            distance = distances[current_position]  # TODO: This may need to be a lambda

        # Trace paths
        next_nodes = {current_position}

        nodes_in_paths = {current_position}
        while next_nodes:
            latest_node = next_nodes.pop()
            nodes_in_paths.add(latest_node)
            for next_node in previous[latest_node]:
                next_nodes.add(next_node)
        
        return distance, nodes_in_paths
    
    def find_path(self, n_bytes: int = -1, visuals: bool = True) -> int:
        """Find the shortest path distance with Dijkstra's"""
        n_bytes -= 1
        distance, nodes_in_paths = self.shortest_dijkstras(n_bytes=n_bytes, visuals=visuals)

        # Visualise maze, with path visible
        if visuals:
            logger.info("> Final State")
            self._display_space(n_bytes=n_bytes, path_nodes=nodes_in_paths)
        return distance

    def find_blocker(self) -> tuple[int, int]:
        """Find the smallest number of bytes that returns math.inf via binary search"""

        too_low = set()
        too_high = set()
        n_range = [0, len(self.incoming_bytes)]
        index_to_byte = {v: k for k, v in self.incoming_bytes.items()}

        while True:
            index = sum(n_range) // 2
            if index in too_low | too_high:
                break
            logger.debug(f"Attempting with index {index} - {too_high=} {too_low=}")
            distance = self.find_path(n_bytes=index, visuals=False)
            logger.debug(f"{distance=}")

            if distance == math.inf:
                # Seek a smaller index
                too_high.add(index)
                n_range[1] = index
            else:
                # Seek a larger index
                too_low.add(index)
                n_range[0] = index

        return ','.join(map(str, index_to_byte[min(too_high)-1]))


tester = PathFinder("./test.txt", memory_space=(0,7))
assert tester.find_path(n_bytes=12) == 22
assert tester.find_blocker() == "6,1"

solver = PathFinder("./input.txt")
print(f"A: {solver.find_path(1024)}")   # 286
print(f"B: {solver.find_blocker()}")    # 20,64
