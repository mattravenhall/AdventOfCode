#!/usr/bin/env python3

from collections import defaultdict


class MonkeyMarket:
    def __init__(self, input_file: str = None) -> None:
        self.monkey_numbers = self._parse_input(input_file)
    
    def _parse_input(self, input_file: str) -> tuple[dict, dict]:
        if input_file is None:
            return []
        return list(map(int, open(input_file).read().strip().split('\n')))

    def _apply_rules(self, secret_number: int) -> int:
        """Apply rules to a secret number"""
        secret_number ^= (secret_number * 64)  # MULTIPLY by 64 and MIX
        secret_number %= 16777216  # PRUNE
        secret_number ^= (secret_number // 32)  # INT-DIVIDE by 32 and MIX
        secret_number %= 16777216  # PRUNE
        secret_number ^= (secret_number * 2048)  # MULTIPLY by 2048 and MIX
        secret_number %= 16777216  # PRUNE
        return secret_number

    def _apply_rules_n_times(self, secret_number: int, n: int, track_all: bool = False) -> int:
        """Apply rules to an initial secret number n times"""
        secret_numbers = []
        for _ in range(n):
            secret_number = self._apply_rules(secret_number)
            if track_all:
                secret_numbers.append(secret_number)
            
        if track_all:
            return secret_numbers
        else:
            return secret_number

    def sum_nth_numbers(self, n=2000) -> int:
        """Solve for Part One"""
        total = 0
        for number in self.monkey_numbers:
            total += self._apply_rules_n_times(number, n)
        return total

    def optimise_banana_market(self) -> int:
        """Solve for Part Two"""
        # For each monkey, scan deltas in groups of four
        # When a seq is first encountered, add to a dict with the latest delta
        # If another monkey has that sequence, add its latest delta
        # Don't overwrite, just take the first encountered
        profits = defaultdict(int)
        for secret_number in self.monkey_numbers:
            deltas = []
            observed: set[tuple] = set()
            number_old = secret_number
            for _ in range(2000):
                number_new = self._apply_rules(number_old)
                price_old = int(str(number_old)[-1])
                price_new = int(str(number_new)[-1])
                deltas.append(price_old - price_new)
                deltas = deltas[-4:]
                if len(deltas) == 4:
                    deltas_t = tuple(deltas)
                    if deltas_t not in observed:
                        observed.add(deltas_t)
                        profits[deltas_t] += price_new
                number_old = number_new
        return profits[max(profits, key=profits.get)]


tester = MonkeyMarket()
assert tester._apply_rules(123) == 15887950
assert tester._apply_rules_n_times(123, 10, track_all=True) == [15887950, 16495136, 527345, 704524, 1553684, 12683156, 11100544, 12249484, 7753432, 5908254]
assert tester._apply_rules_n_times(1, 2000) == 8685429
assert tester._apply_rules_n_times(10, 2000) == 4700978
assert tester._apply_rules_n_times(100, 2000) == 15273692
assert tester._apply_rules_n_times(2024, 2000) == 8667524
assert MonkeyMarket('./test.txt').optimise_banana_market() == 23

print(f"A: {MonkeyMarket('./input.txt').sum_nth_numbers()}")
print(f"B: {MonkeyMarket('./input.txt').optimise_banana_market()}")
