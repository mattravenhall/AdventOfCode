#!/usr/bin/env python3

from typing import Union
import re


def standardise(string: Union[str, int]) -> str:
	str_to_int = {
		"one": "1",
		"two": "2",
		"three": "3",
		"four": "4",
		"five": "5",
		"six": "6",
		"seven": "7",
		"eight": "8",
		"nine": "9",
	}
	return str_to_int.get(string, string)


re_numerics = r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))"

total = 0

for line in open("input.txt").readlines():
	line = line.strip()
	numbers = re.findall(re_numerics, line)
	print(f"{line}: {numbers}")

	if numbers:
		digit = int(standardise(numbers[0]) + standardise(numbers[-1]))
		total += digit
		print(f"{digit} - {total}")


print(total)
