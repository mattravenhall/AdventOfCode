import pandas as pd

codes_with_2 = 0
codes_with_3 = 0

for line in open('input.txt'):
	letter_counts = list(pd.Series(list(line)).value_counts())
	codes_with_2 += 2 in letter_counts
	codes_with_3 += 3 in letter_counts

print('2: {0}\n3: {1}'.format(codes_with_2, codes_with_3))
print(codes_with_2 * codes_with_3)
