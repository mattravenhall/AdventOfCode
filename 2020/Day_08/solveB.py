#!/usr/bin/env python3

# Welcome to the most over-engineered 'solution' ever

import sys
from collections import OrderedDict


class CommandPathFixer():
    def __init__(self, filename):
        self.filename = filename
        self.commands = [command.strip().split() for command in open(filename).readlines()]
        self.index = 0
        self.accumulator = 0
        self.inf_loop = False
        self.command_path = OrderedDict()
        self.total = 0
        self.fix_attempts = set()
        self.modified = None
        self.fix = None

    def run(self):
        self.fix_command_path(0)
        self.calc_accumulator()
        print(self.total)

    def calc_accumulator(self):
        total = 0
        for operation, argument in self.command_path.values():
            if operation == 'acc':
                total += int(argument)
        self.total = total

    def fix_command_path(self, index):
        # Update command_path
        operation, argument = self.commands[index]
        self.command_path[index] = (operation, argument)
        # print(f"CommandPath: {[x for x in self.command_path.items()]}")

        # Identify next index
        if operation == 'jmp':
            index += int(argument)
        else:
            index += 1

        if index == len(self.commands):
            return self.command_path

        if (index in self.command_path.keys()) or (index > len(self.commands)):
            # print(f"> InfLoop Detected [{index}] {self.command_path[index]} <")
            reversed_path = [c for c in reversed(self.command_path.keys())]
            for path_idx in reversed_path:
                operation, argument = self.command_path[path_idx]
                discarded = self.command_path.pop(path_idx)

                if operation == 'acc' or path_idx in self.fix_attempts:
                    # print(f"Discarding: {discarded}")
                    if path_idx == self.modified:
                        # print(f'Cleaning {path_idx}')
                        self.modified = None
                    continue

                new_operation = 'jmp' if discarded[0] == 'nop' else 'nop'
                modified = (new_operation, discarded[1])

                self.fix_attempts.add(path_idx)
                # print(f"Attempting fix: {discarded} -> {modified}")

                # Prevent >1 modification
                if self.modified is None:
                    self.modified = path_idx
                    self.command_path[path_idx] = modified
                else:
                    # If attempting a second modification, back out
                    continue

                if new_operation == 'jmp':
                    # Convert a jmp into a nop
                    index = path_idx + int(argument)
                elif new_operation == 'nop':
                    # Convert a nop into a jmp
                    index = path_idx + 1

                attempted_fix = self.fix_command_path(index)
                if attempted_fix is not False:
                    if self.fix is None:
                        self.fix = f"[{path_idx}] {discarded} -> {modified}"
                    return attempted_fix
                return False
        else:
            return self.fix_command_path(index)


if __name__ == '__main__':
    FILENAME = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    fixer = CommandPathFixer(FILENAME)
    fixer.run()
