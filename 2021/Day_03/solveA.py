#!/usr/bin/env python3

import pandas as pd

report = pd.read_csv('input.txt', header=None, dtype=str)[0].apply(lambda x: pd.Series(list(x)))

gamma = int(''.join(report.apply(lambda x: x.value_counts().index[0])), 2)
epsilon = int(''.join(report.apply(lambda x: x.value_counts().index[-1])), 2)

power_consumption = gamma * epsilon

print(power_consumption)

