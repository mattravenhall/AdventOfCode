import numpy as np

def calcCellPower(x, y, gridID):
	rackID = x+10
	power = ((rackID * y) + gridID) * rackID
	power = int(str(power)[-3] if len(str(power)) >= 3 else 0) - 5
	return(power)

gridSize = 300
gridID = 5034

grid = np.zeros([gridSize, gridSize])
for i in range(gridSize):
	for j in range(gridSize):
		grid[i][j] = calcCellPower(i+1, j+1, gridID)

def timeFunc(func, ID='', file=''):
	import time
	t0 = time.time()
	res = eval(func)
	t1 = time.time()
	if ID != '':
		print('[{}] TimeTaken: {}'.format(ID, t1-t0))		
	elif file != '':
		with open(file, 'a') as f:
			f.write('{}\n'.format(t1-t0))
	else:
		print('TimeTaken: {}'.format(t1-t0))
	return(res)

sum_max = 0
for sumSize in range(1, 300):
	for i in range(gridSize-sumSize):
		for j in range(gridSize-sumSize):
			sum_ij = grid[i:i+sumSize,j:j+sumSize].sum()
			if sum_ij > sum_max:
				sum_max = sum_ij
				max_x, max_y = i+1, j+1
				sum_size = sumSize

#print('sum_max: {}'.format(sum_max))
print(max_x, max_y, sum_size)