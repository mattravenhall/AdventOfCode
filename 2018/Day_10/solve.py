import re
import numpy as np
import matplotlib.pyplot as plt

position = []
velocity = []

for line in open('input.txt'):
	position.append(list(map(int, re.split(r'(<.+?>)', line)[1].strip('<>').split(','))))
	velocity.append(list(map(int, re.split(r'(<.+?>)', line)[3].strip('<>').split(','))))

posX = np.array(position)[:,0]
posY = np.array(position)[:,1]
velX = np.array(velocity)[:,0]
velY = np.array(velocity)[:,1]

gridsize = [np.inf, np.inf-1]

while gridsize[-1] <= gridsize[-2]:
	posX += velX
	posY += velY

	gridsize.append((max(posX)-min(posX)) * (max(posY)-min(posY)))
#	print(gridsize[-1])

print('Time: {}'.format(len(gridsize)-3))

plt.scatter(posX-velX, -(posY-velY))
plt.show()