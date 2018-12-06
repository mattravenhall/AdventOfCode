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
def sumDist(xy, coords):
	sumDist = 0
	for i, c in enumerate(coords):
		sumDist += manhattan(xy, c)
	return(sumDist)

# Loop through full range
for x in range(0, x_max):
	for y in range(0, y_max):
		mapped[x, y] = sumDist([x, y], coords)

print(len([x for x in mapped.flatten() if x < 10000]))
