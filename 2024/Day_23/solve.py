#!/usr/bin/env python3

from collections import defaultdict


class LANPartyFinder:
    def __init__(self, input_file: str = None) -> None:
        self.graph = self._parse_input(input_file)
    
    def _parse_input(self, input_file: str) -> dict:
        graph = defaultdict(set)
        for pair in open(input_file).readlines():
            c1, c2 = pair.strip().split('-')
            graph[c1].add(c2)
            graph[c2].add(c1)
        return dict(graph)

    def find_t_triplets(self):
        """Part One: Count the set of triplets with a t node"""
        t_triplets = set()
        for node_1 in self.graph:
            if node_1[0] != 't':
                continue
            for node_2 in self.graph[node_1]:
                for node_3 in self.graph[node_1] & self.graph[node_2]:
                    t_triplets.add(tuple(sorted([node_1, node_2, node_3])))
        return len(t_triplets)

    def find_largest_cluster_password(self) -> str:
        """Part Two: Find the largest fully connected cluster, then sort and concat its members."""
        largest_cluster = set()
        considered = set()
        for node_1 in self.graph:
            if node_1 in considered:
                continue
            for node_2 in self.graph[node_1]:
                nodes_shared = self.graph[node_1] & self.graph[node_2]
                if len(nodes_shared) < 1:
                    continue
                cluster = {node_1, node_2} | nodes_shared
                if len(cluster) < len(largest_cluster):
                    continue
                for node in nodes_shared:
                    rest_of_cluster = cluster - {node}
                    # If this node isn't connected to all other nodes, exit
                    if not rest_of_cluster.issubset(self.graph[node]):
                        break
                else:
                    # Complete cluster found
                    largest_cluster = cluster
        return ','.join(sorted(largest_cluster))


test_finder = LANPartyFinder("./test.txt")
assert test_finder.find_t_triplets() == 7
assert test_finder.find_largest_cluster_password() == "co,de,ka,ta"

solver = LANPartyFinder("./input.txt")
print(f"A: {solver.find_t_triplets()}")
print(f"B: {solver.find_largest_cluster_password()}")
