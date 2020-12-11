import numpy as np

# Read input file, convert to edge tuples
edges = np.array([(x.split(' ')[1], x.split(' ')[7]) for x in open('input.txt')])

# Define features
nodes = list(set(edges.flatten()))

seq = ''
while len(nodes) > 0:
	children = edges[:,1]
	orphans = list(set(nodes) - set(children))
	orphans.sort()
	seq += nodes.pop(nodes.index(orphans[0]))
	edges = np.array([list(e) for e in edges if e[0] not in list(seq)])
	if len(nodes) == 1:
		seq += nodes.pop(0)

print(seq)