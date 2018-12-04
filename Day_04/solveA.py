import pandas as pd

# Read input (removing year because of time period issues)
raw_input = [line.strip().strip('[')[5:].split('] ') for line in open('input.txt')]

# Order chronologically
logs = pd.DataFrame(raw_input).sort_values(0)
logs.columns = ['Time', 'Info']
logs['Time'] = pd.to_datetime(logs['Time'], format='%m-%d %H:%M')
logs.reset_index()

# Loop logs
sleepytimes = {}
guard = ''
start = 0
end = 0

# Convert to sleep tracks
for index in range(logs.shape[0]):
	# Grab correct details
	if logs.iloc[index]['Info'].startswith('Guard'):
		guard = logs.iloc[index]['Info'].split('#')[1].split(' ')[0]
		start = 0
		end = 0
	elif logs.iloc[index]['Info'] == 'falls asleep':
		start = logs.iloc[index]['Time'].minute
		end = 0
	elif logs.iloc[index]['Info'] == 'wakes up':
		end = logs.iloc[index]['Time'].minute

	# Assign sleeptrack to guard
	if start >= end:
		continue

	if guard not in sleepytimes:
		sleepytimes[guard] = [x for x in range(start, end)]
	else:
		sleepytimes[guard].extend([x for x in range(start,end)])

# Most commonly asleep guard
sleepLengths = {x: len(sleepytimes[x]) for x in sleepytimes}
topSleeper = max(sleepLengths, key=sleepLengths.get)

# Time most sleepy guard was most asleep
topSleeper_times = dict(pd.Series(sleepytimes[topSleeper]).value_counts())
topMinute = max(topSleeper_times, key=topSleeper_times.get)

# ID of guard * minute most asleep
print(logs)
print()
print(sleepytimes)
print()
print('Guard: {}'.format(topSleeper))
print('Minute: {}'.format(topMinute))
print(int(topSleeper) * topMinute)
