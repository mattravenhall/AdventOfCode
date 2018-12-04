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

# Find most common guard-time combination
top_count = 0
top_guard = ''
top_time = ''

for guard in sleepytimes.keys():
	guard_sleeps = dict(pd.Series(sleepytimes[guard]).value_counts())
	timepoint = max(guard_sleeps, key=guard_sleeps.get)
	count = guard_sleeps[timepoint]
	if count > top_count:
		top_count = count
		top_guard = guard
		top_time = timepoint

print('Guard: {}'.format(top_guard))
print('Time: {}'.format(top_time))
print(int(top_guard) * top_time)
