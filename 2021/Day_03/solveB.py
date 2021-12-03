#!/usr/bin/env python3

import pandas as pd


def find_entry(report: pd.DataFrame, high: bool) -> str:
	for i in range(len(report.columns)):
		bit_counts = report[i].value_counts()
		if len(set(report[i])) == 1:
			continue
		if len(set(bit_counts.values)) == 1:
			bit_of_interest = '1' if high else '0'
		else:
			bit_of_interest = bit_counts.index[0 if high else -1]
		report = report[report[i] == bit_of_interest]
		if report.shape[0] == 1:
			return int(''.join(report.values[0]), 2)


report = pd.read_csv('input.txt', header=None, dtype=str)[0].apply(lambda x: pd.Series(list(x)))

oxygen_generator = find_entry(report, True)
CO2_scrubber = find_entry(report, False)

life_support = oxygen_generator * CO2_scrubber

print(life_support)
