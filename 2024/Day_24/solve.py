#!/usr/bin/env python3

import logging
import math

import matplotlib.pyplot as plt
import networkx as nx

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


class JungleGates:
    def __init__(self, input_file: str = None, override_x = None, override_y = None, swaps: set[tuple] = set(), name = 'test') -> None:
        self.name = name
        self.swaps = self._build_swap_dict(swaps)
        self.gates, rules = self._parse_input(input_file, override_x, override_y)
        self._apply_rules(rules)

    @staticmethod
    def _build_swap_dict(swaps: set[tuple]) -> dict:
        swap_dict = {}
        for pair_a, pair_b in swaps:
            swap_dict[pair_a] = pair_b
            swap_dict[pair_b] = pair_a
        return swap_dict

    def _parse_input(self, input_file: str, override_x = None, override_y = None) -> dict:
        graph = nx.DiGraph()
        gates = {}
        setup = True
        rules = []

        # Setup up initial states and collect rules
        for line in open(input_file):
            if line == '\n':
                # Apply input overrides here
                if override_x is not None:
                    x_gates = sorted([gate for gate in gates if gate.startswith('x')])
                    n_x_gates = len(x_gates)
                    bin_x = bin(override_x)[2:].zfill(n_x_gates)
                    for i, gate in enumerate(x_gates):
                        gates[gate] = bool(int(bin_x[i]))

                if override_y is not None:
                    y_gates = sorted([gate for gate in gates if gate.startswith('y')])
                    n_y_gates = len(y_gates)
                    bin_y = bin(override_y)[2:].zfill(n_y_gates)
                    for i, gate in enumerate(y_gates):
                        gates[gate] = bool(int(bin_y[i]))

                setup = False
                continue
            if setup:
                gate, state = line.strip().split(':')
                gates[gate] = bool(int(state))
            else:
                gate_a, relation, gate_b, _, gate_out = line.strip().split(' ')

                # Apply swaps here
                if gate_out in self.swaps.keys():
                    gate_out = self.swaps[gate_out]

                # Update gates
                for gate in [gate_a, gate_b]:
                    if gate not in gates.keys():
                        gates[gate] = None

                # Collect graph for visualisation
                graph.add_node(gate_a, label=gate_a, node_shape='o')
                graph.add_node(gate_b, label=gate_b, node_shape='o')
                graph.add_node(f"{relation} {gate_a}-{gate_b}", label=relation, node_shape='d')
                graph.add_node(gate_out, label=gate_out, node_shape='o')
                graph.add_edges_from([
                    (gate_a, f"{relation} {gate_a}-{gate_b}"),
                    (gate_b, f"{relation} {gate_a}-{gate_b}"),
                    (f"{relation} {gate_a}-{gate_b}", gate_out),
                ])

                # Record rule
                rules.append([gate_a, gate_b, relation, gate_out, False])
        
        self._visualise_graph(graph, filename=self.name)

        return gates, rules

    @staticmethod
    def _visualise_graph(graph, filename: str):
        color_map = []
        node_shapes = []
        for node in graph:
            if node.startswith('x'):
                color_map.append('indianred')
            elif node.startswith('y'):
                color_map.append('powderblue')
            elif node.startswith('z'):
                color_map.append('slateblue')
            elif node.startswith('XOR') or node.startswith('AND') or node.startswith('OR'):
                color_map.append('seagreen')
            else:
                color_map.append('palegoldenrod')

        
        node_shapes = nx.get_node_attributes(graph, 'node_shape')
        node_shapes = [value for _, value in node_shapes.items()]

        fig, ax = plt.subplots(1, 1, figsize=(15, 40), constrained_layout=True)
        nx.draw(
            graph,
            pos=nx.nx_agraph.graphviz_layout(graph, prog="dot"), #nx.nx_agraph.graphviz_layout(graph)
            node_color=color_map,
            node_size=140,
        )

        nx.draw_networkx_labels(
            graph,
            pos=nx.nx_agraph.graphviz_layout(graph, prog="dot"), #nx.nx_agraph.graphviz_layout(graph),
            labels=nx.get_node_attributes(graph, 'label'),
            font_size=5,
            font_family='sans-serif'
        )
        ax.set_facecolor('cadetblue')
        ax.axis('off')
        fig.set_facecolor('cadetblue')
        plt.savefig(f"{filename}.png", dpi=400, bbox_inches='tight', pad_inches = 0)

    def _apply_rules(self, rules):
        # Apply rules
        rules_remaining = math.inf
        while rules_remaining > 0:
            rules_remaining = 0
            for rule in rules:
                # Skip completed rules
                if rule[-1]:
                    continue

                # Apply rule, update tracking state (True=rule applied, False=rule not applied)
                rule[-1] = self._apply_rule(*rule[:-1])

                # Log if a rule couldn't be completed
                if not rule[-1]:
                    rules_remaining += 1

    def _apply_rule(self, gate_a: str, gate_b: str, relation: str, gate_out: str) -> bool:
        """Apply a specific rule, return True/False to indicate success"""

        logger.debug(f"Applying rule {gate_a} {relation} {gate_b} -> {gate_out}")

        # Abort if neither input gate lacks a value
        if self.gates[gate_a] is None or self.gates[gate_b] is None:
            # logger.debug(f"Missing input gate")
            return False

        if self.gates.get(gate_out) is not None:
            raise ValueError(f"Output gate {gate_out} is already set to {self.gates[gate_out]}")
        
        # Apply rule
        if relation == "AND":
            self.gates[gate_out] = self.gates[gate_a] and self.gates[gate_b]
        elif relation == "OR":
            self.gates[gate_out] = self.gates[gate_a] or self.gates[gate_b]
        elif relation == "XOR":
            self.gates[gate_out] = self.gates[gate_a] ^ self.gates[gate_b]
        else:
            raise ValueError(f"Unknown relation: {relation}")
    
        return True
    
    def identify_z_number(self):
        """Solve for Part One"""
        z_gates = {key: value for key, value in self.gates.items() if key.startswith('z')}

        z_number = ''
        for gate_id in range(len(z_gates.keys())):
            z_number += str(int(z_gates[f"z{gate_id:02}"]))
        
        return int(z_number[::-1], 2)


assert JungleGates("./test.txt", name='test').identify_z_number() == 2024
print(f"A: {JungleGates('./input.txt', name='input').identify_z_number()}")  # 49430469426918
# For Part Two, we switch the candidates I manually identified from the output graphs
assert JungleGates('./input.txt', swaps=[('pbv', 'z16'), ('qqp', 'z23'), ('fbq', 'z36'), ('qnw', 'qff')], name='fixed').identify_z_number() == 49499197294310
