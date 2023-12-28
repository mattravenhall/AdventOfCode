#!/usr/bin/env python3

from abc import ABC
from collections import defaultdict
import re
from queue import Queue
from typing import Literal


global pulses_sent
pulses_sent = {
    "high": 0,
    "low": 0,
}

global pulse_queue
pulse_queue = Queue()


class Module(ABC):
    def __init__(self, name: str, destinations: list[str], *args, **kwargs):
        self.name = name
        self.destinations = destinations.split(', ')

    def send_pulse(self, strength: Literal['high', 'low']):
        for destination in self.destinations:
            print(f"{self.name} -{strength}-> {destination}")
            pulses_sent[strength] += 1

            if destination not in modules:
                # print(f"Send pulse to unobserved deadend module '{destination}'")
                return

            # Add pulses to pulse queue
            pulse_queue.put((self.name, destination, strength))
    
    def receive_pulse(self, strength: Literal['high', 'low'], input: str):
        raise NotImplementedError        


class Button(Module):
    """Unique module, sends a pulse to the broadcaster node"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def receive_pulse(self, strength: Literal['high', 'low'], input: str):
        raise ValueError("Button received an input pulse")


class Broadcaster(Module):
    """Unique broadcaster, when pulsed, sends the same"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def receive_pulse(self, strength: Literal['high', 'low'], input: str):
        # print(f"Module {self.name} received {strength} pulse from {input}")
        self.send_pulse(strength)


class FlipFlop(Module):
    """Flip-Flop (%) - initially off, ignores high signals, flips on/off with low signals"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = 0

    def receive_pulse(self, strength: Literal['high', 'low'], input: str):
        # print(f"Module {self.name} received {strength} pulse from {input}")
        if strength == 'high':
            # Ignore high pulses
            return
        else:
            # Flip on/off
            self.state = 1 - self.state

        # Send high if state is now on, else send low
        self.send_pulse("high" if self.state else "low")


class Conjunction(Module):
    """Conjunction (&) - remembers last input pulses (initially low), sends reverse of last received"""
    def __init__(self, *args, inputs, **kwargs):
        super().__init__(*args, **kwargs)
        self.memory = {input: "low" for input in inputs}
    
    def receive_pulse(self, pulse: Literal["high", "low"], input: str):
        # print(f"Module {self.name} received {strength} pulse from {input}")
        self.memory[input] = pulse
        # print(f"Module {self.name} recorded memory for {input} as {pulse}")

        if set(self.memory.values()) == {"high"}:
            self.send_pulse("low")
        else:
            self.send_pulse("high")


module_inputs = defaultdict(set)
modules: dict[Module] = {}
conjunctions = set()

# Create all modules
modules['button'] = Button('button', 'broadcaster')
for line in open("input.txt").readlines():
    mtype, name, destinations = re.findall(r'^([%&])?(\w+) -> (.*)', line.strip())[0]

    # Collect all individual connections
    for destination in destinations.split(', '):
        module_inputs[destination].add(name)

    # Create required module (Conjunctions are created when all inputs are known)
    if mtype == '':
        modules[name] = Broadcaster(name, destinations)
    elif mtype == '%':
        modules[name] = FlipFlop(name, destinations)
    elif mtype == '&':
        conjunctions.add((name, destinations))
        # modules[name] = Conjunction(destinations=destinations)
    else:
        raise ValueError(f"Unknown mtype: '{mtype}'")


# Create Conjunction modules
for name, destinations in conjunctions:
    modules[name] = Conjunction(
        name,
        destinations,
        inputs = module_inputs[name],
    )


def press_button(strength: Literal['low', 'high'] = 'low'):
    modules['button'].send_pulse('low')
    # modules['broadcaster'].receive_pulse('low', input='button')
    while not pulse_queue.empty():
        sender, receiver, strength = pulse_queue.get()
        modules[receiver].receive_pulse(strength, sender)
        # print(f"Queue size: {pulse_queue.qsize()}", end='\r')


def solveA():
    for i in range(1000):
        # print(f"Pressed {i+1} time{'s' if i + 1 != 1 else ''}")
        press_button()
    
    return pulses_sent['high'] * pulses_sent['low']


print(solveA())
