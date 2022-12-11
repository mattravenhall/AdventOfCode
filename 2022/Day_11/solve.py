#!/usr/bin/env python3.10

import math


class Troop:
    """A collection of Monkey objects"""

    def __init__(self, filename: str):
        self.members = {}
        self._process_commands(filename)

    def _process_commands(self, filename: str):
        monkey_config: dict = {}
        for line in open(filename).readlines():
            line = line.strip()

            if line.startswith("Monkey "):
                monkey_id = int(line.strip(':').split()[1])
                monkey_config["id"] = int(monkey_id)
                continue

            match line.split(':'):
                case ["Starting items", items]:
                    monkey_config["items"] = [
                        item for item in map(int, items.strip().split(', '))
                    ]
                case ["Operation", operation_string]:
                    monkey_config["operation_string"] = operation_string.strip()[6:]
                case ["Test", test_div]:
                    monkey_config["test_div"] = int(test_div.split(' ')[-1])
                case ["If true", test_true]:
                    monkey_config["test_true"] = int(test_true.split(' ')[-1])
                case ["If false", test_false]:
                    monkey_config["test_false"] = int(test_false.split(' ')[-1])
                case ['']:
                    self.add_member(monkey_config)
                    monkey_config = {}
                case _:
                    breakpoint()

        if monkey_config:
            self.add_member(monkey_config)

    def add_member(self, monkey_config: dict) -> None:
        self.members[monkey_config["id"]] = Monkey(
            name=monkey_config["id"],
            items=monkey_config["items"],
            operation_str=monkey_config["operation_string"],
            test_config=[
                monkey_config["test_div"],
                monkey_config["test_true"],
                monkey_config["test_false"],
            ]
        )

    def simulate_rounds(self, n_rounds: int, part_one: bool):
        lcm = math.lcm(*[
            monkey.divisible for monkey in self.members.values()
        ])

        for round in range(n_rounds):
            for monkey_id in sorted(self.members.keys()):
                monkey = self.members[monkey_id]

                # If a monkey is holding no items, its turn ends
                if not monkey.items:
                    continue

                # Check which items to throw
                for item in sorted(monkey.items):
                    # print(f"Monkey inspects an item with worry level of {item}")
                    if part_one:
                        worry = int(monkey.inspect_item(item) / 3)
                    else:
                        worry = int(monkey.inspect_item(item) % lcm)
                    # print(f"Worry level increases to {worry}")
                    throw_to = monkey.test_item(worry)
                    # print(f"Item with worry level {worry} is thrown to monkey {throw_to}")
                    self.members[throw_to].items.append(worry)

                # At this point all items have been thrown
                monkey.items = []

            # print(f"After round {round+1}, monkeys are holding:")
            # self.view_items()

    def view_items(self):
        for monkey_id in sorted(self.members.keys()):
            print(f"Monkey {monkey_id}: {', '.join(map(str, self.members[monkey_id].items))}")

    def view_inspections(self):
        for monkey_id in sorted(self.members.keys()):
            print(f"Monkey {monkey_id} inspected items {self.members[monkey_id].n_inspections} times.")

    def calc_monkey_business(self):
        n_inspections = [
            monkey.n_inspections for i, monkey in self.members.items()
        ]
        monkey_business = math.prod(sorted(n_inspections)[-2:])
        return monkey_business


class Monkey:
    """An individual monkey"""

    def __init__(self, name: int, items: list[int], operation_str: str, test_config: list[int]):
        self.id = name
        self.items = sorted(items)
        self.operation_str = operation_str
        self.divisible, self.test_true, self.test_false = test_config
        self.n_inspections: int = 0

    def inspect_item(self, old: int) -> int:
        """Determine updated item worry level"""
        new = eval(self.operation_str)
        self.n_inspections += 1
        return new

    def test_item(self, item: int):
        """Identify monkey to test item to"""
        return self.test_true if item % self.divisible == 0 else self.test_false


def solveA(filename: str) -> int:
    troop = Troop(filename)
    troop.simulate_rounds(20, part_one=True)

    return troop.calc_monkey_business()


def solveB(filename: str) -> int:
    troop = Troop(filename)
    troop.simulate_rounds(10000, part_one=False)

    # troop.view_inspections()

    return troop.calc_monkey_business()


if __name__ == '__main__':
    assert solveA("test.txt") == 10605
    print(f'A: {solveA("input.txt")}')

    assert solveB("test.txt") == 2713310158
    print(f'B: {solveB("input.txt")}')
