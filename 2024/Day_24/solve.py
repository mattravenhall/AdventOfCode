#!/usr/bin/env python3

import logging
import math

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')


class JungleGates:
    def __init__(self, input_file: str = None) -> None:
        self.gates, rules = self._parse_input(input_file)
        self._apply_rules(rules)

    def _parse_input(self, input_file: str) -> dict:
        gates = {}
        setup = True
        rules = []

        # Setup up initial states and collect rules
        for line in open(input_file):
            if line == '\n':
                setup = False
                continue
            if setup:
                gate, state = line.strip().split(':')
                gates[gate] = bool(int(state))
            else:
                gate_a, relation, gate_b, _, gate_out = line.strip().split(' ')

                for gate in [gate_a, gate_b]:
                    if gate not in gates.keys():
                        gates[gate] = None
                
                rules.append([gate_a, gate_b, relation, gate_out, False])
        
        return gates, rules

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

        # logger.debug(f"Applying rule {gate_a} {relation} {gate_b} -> {gate_out}")

        # Abort if neither input gate lacks a value
        if self.gates[gate_a] is None or self.gates[gate_b] is None:
            # logger.debug(f"Missing input gate")
            return False

        if self.gates.get(gate_out) is not None:
            breakpoint()
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


assert JungleGates("./test.txt").identify_z_number() == 2024

print(f"A: {JungleGates('./input.txt').identify_z_number()}")  # 49430469426918



## Four pairs of gates were swapped (no shared, so that's 8 gates)
