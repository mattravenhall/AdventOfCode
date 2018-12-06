import numpy as np
import pandas as pd

# Clean up coordinates
coords = np.array([list(map(int, line.strip().split(', '))) for line in open('input.txt').readlines()])

# Identify full range dimensions
x_max = coords[:, 0].max()+1
y_max = coords[:, 1].max()+1
mapped = np.zeros((x_max, y_max))
border = set()

# Manhattan distance
def manhattan(xy, ij):
	return(abs(xy[0] - ij[0]) + abs(xy[1] - ij[1]))

# Area determination (lowest Manhattan distanct)
def findArea(xy, coords):
	area = []
	minDist = np.inf

	for i, c in enumerate(coords):
		dist = manhattan(xy, c)

		if dist < minDist:
			minDist = dist
			area = [i]
		elif dist == minDist:
			area.append(i)

	return(None) if len(area) != 1 else area[0]

# Loop through full range
for x in range(0, x_max):
	for y in range(0, y_max):
		mapped[x, y] = findArea([x, y], coords)

# Determine infinite (border) regions
infinite = [int(x) for x in set(mapped[0]) | set(mapped[-1]) | set(mapped[:,0]) | set(mapped[:,-1]) if not np.isnan(x)]
finite = [x for x in range(len(coords)) if x not in infinite]

##print(mapped)
print(max(pd.Series(mapped.flatten()).value_counts()[finite]))
