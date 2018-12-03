import numpy as np

def processID(line):
	return(line.split('@')[1].strip().replace(': ',',').replace('x',','))

Xgaps = []
Ygaps = []
Xwidths = []
Ywidths = []

for line in open('input.txt'):
	Xgap, Ygap, Xwidth, Ywidth = processID(line).split(',')
	Xgaps.append(int(Xgap))
	Ygaps.append(int(Ygap))
	Xwidths.append(int(Xwidth))
	Ywidths.append(int(Ywidth))

assert len(Xgaps) == len(Ygaps) == len(Xwidths) == len(Ywidths), 'Length mismatch'

maxX = max(np.array(Xgaps) + np.array(Xwidths))
maxY = max(np.array(Ygaps) + np.array(Ywidths))
fabric = np.zeros((maxX, maxY))

for i in range(len(Xgaps)):
	for x in range(Xgaps[i], Xgaps[i]+Xwidths[i]):
		for y in range(Ygaps[i], Ygaps[i]+Ywidths[i]):
			fabric[x][y] += 1

#print(fabric)
print(sum([sum([square >= 2 for square in line]) for line in fabric]))
