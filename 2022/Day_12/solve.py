#!/usr/bin/env python3

import math
import string
import random


class Graph:
	def __init__(self, filename: str):
		self.flags = {
			"S": -1,
			"E": 26,
		}
		self.nodes = self._load_graph(filename)

	def _load_graph(self, filename: str) -> list[tuple[int, int]]:
		nodes: dict = {}

		# Collect and place all nodes
		for y, row in enumerate(open(filename).readlines()):
			for x, value in enumerate(row.strip()):
				nodes[(x, y)] = {
					"coords": (x, y),
					"value": value,
					"height": self._val2height(value),
					"parents": set(),
					"children": set(),
				}

				if value == 'S':
					self.source = (x, y)
				elif value == 'E':
					self.target = (x, y)

		# Now identify valid neighbours
		for x, y in nodes.keys():
			core_node = nodes[(x, y)]
			neighbour_coords = [
				(x, y-1),
				(x, y+1),
				(x-1, y),
				(x+1, y),
			]
			for coords in neighbour_coords:
				neighbour = nodes.get(coords, None)
				if neighbour is None:
					pass
				else:
					if neighbour["height"] == core_node["height"]:
						core_node["parents"].add(coords)
						core_node["children"].add(coords)
					elif neighbour["height"] <= core_node["height"] + 1:
						# Valid children are no more than one higher
						core_node["children"].add(coords)
					else:
						# All others are parents
						core_node["parents"].add(coords)
		return nodes

	def _val2height(self, value: str) -> int:
		if value in self.flags.keys():
			return self.flags[value]
		else:
			return string.ascii_lowercase.index(value)

	def shortest_bfs(self) -> int:
		# Breadth-first search: https://en.wikipedia.org/wiki/Breadth-first_search
		previous = {self.source: None}
		queue = [self.source]

		while queue:
			current = queue.pop(0)

			if current == self.target:
				break

			for child in self.nodes[current]['children']:
				if child not in previous:
					queue.append(child)
					previous[child] = current

		# Build path
		path = []
		current = self.target
		while current != self.source:
			path.append(current)
			current = previous[current]

		return len(path)

	def shortest_dijkstras(self) -> int:
		# Dijkstra's algorithm: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

		# Distance from source node
		distances = {
			node: math.inf for node in self.nodes
		}
		distances[self.source] = 0

		# Path parent
		previous = {
			node: None for node in self.nodes
			if node != self.source
		}

		# Set of visited nodes
		unvisited = {
			node for node in self.nodes
			# if node != self.source
		}

		while unvisited:
			# Set current node to a node with the lowest distance to source
			# print(f"Selecting new current node")
			current = self.nodes[min(unvisited, key=distances.get)]
			current_distance = distances[current['coords']]

			# Set current node as visited
			# print(f"Deleting {current['coords']} from unvisited")
			unvisited.remove(current['coords'])

			if current['coords'] == self.target:
				# print(f"Located target node")
				break

			# print(f"Current node is now {current['coords']}")
			# print(f"Current distance is now {current_distance}")

			# Consider nodes adjacent to current node
			for child in current["children"]:
				# print(f"Considering child {child}")

				# Skip if child has already been visited
				if child not in unvisited:
					# print(f"Child {child} is in visited")
					continue

				# All node-node distances are 1
				new_distance = distances[current['coords']] + 1

				# Update child's distance if new distance is lower
				if new_distance < distances[child]:
					distances[child] = new_distance
					previous[child] = current['coords']

		# Build path
		path = []
		current = self.target
		while current != self.source:
			path.append(current)
			current = previous[current]

		return len(path)

		return distances[self.target]


def solveA(filename:str) -> int:
	# Parse input into a graph
	graph = Graph(filename)

	# Use Dijkstra's algo to find shortest path
	return graph.shortest_dijkstras()


if __name__ == '__main__':
	assert solveA("test.txt") == 31

	print(solveA("input.txt"))
