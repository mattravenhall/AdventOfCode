import numpy as np

def calcCellPower(x, y, gridID):
	rackID = x+10
	power = ((rackID * y) + gridID) * rackID
	power = int(str(power)[-3] if len(str(power)) >= 3 else 0) - 5
	return(power)

gridSize = 300
gridID = 5034

sumSize = 3
grid = np.zeros([gridSize, gridSize])
for i in range(gridSize):
	for j in range(gridSize):
		grid[i][j] = calcCellPower(i+1, j+1, gridID)

sum_max = 0
for i in range(gridSize-sumSize):
	for j in range(gridSize-sumSize):
		sum_ij = np.sum(grid[i:i+3,j:j+3])
		if sum_ij > sum_max:
			sum_max = sum_ij
			max_x, max_y = i+1, j+1

#print('sum_max: {}'.format(sum_max))
print(max_x, max_y)