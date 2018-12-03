import numpy as np

def processID(line):
	return(line.split('@')[1].strip().replace(': ',',').replace('x',',')+','+line.split('@')[0].strip().lstrip('#'))

Xgaps = []
Ygaps = []
Xwidths = []
Ywidths = []
IDs = []

for line in open('input.txt'):
	Xgap, Ygap, Xwidth, Ywidth, ID = processID(line).split(',')
	Xgaps.append(int(Xgap))
	Ygaps.append(int(Ygap))
	Xwidths.append(int(Xwidth))
	Ywidths.append(int(Ywidth))
	IDs.append(ID)

assert len(Xgaps) == len(Ygaps) == len(Xwidths) == len(Ywidths), 'Length mismatch'

maxX = max(np.array(Xgaps) + np.array(Xwidths))
maxY = max(np.array(Ygaps) + np.array(Ywidths))
fabric = np.empty((maxX, maxY), dtype="S10")
fabric[:] = '.'
nonOverlaps = IDs.copy()

for i in range(len(Xgaps)):
	for x in range(Xgaps[i], Xgaps[i]+Xwidths[i]):
		for y in range(Ygaps[i], Ygaps[i]+Ywidths[i]):
			if fabric[x][y].decode() == '.':
				fabric[x][y] = IDs[i]
			elif fabric[x][y].decode() in nonOverlaps:
				if IDs[i] in nonOverlaps:
					nonOverlaps.remove(IDs[i])
				nonOverlaps.remove(fabric[x][y].decode())
			elif fabric[x][y].decode() not in nonOverlaps:
				if IDs[i] in nonOverlaps:
					nonOverlaps.remove(IDs[i])
				fabric[x][y] = 'X'

#print(fabric)
#print(sum([sum([square >= 2 for square in line]) for line in fabric]))
print(nonOverlaps[0]) if len(nonOverlaps) == 1 else nonOverlaps
