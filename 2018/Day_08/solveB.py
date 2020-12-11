# Day 8, Part 2

seq = [int(x) for x in open('input.txt').read().strip().split()]

def downOne(seq):
	mSum = 0
	while len(seq) > 0:
		nChild = seq.pop(0)
		nMetric = seq.pop(0)
		childValues = []

		if nChild > 0:
			for _ in range(nChild):
				data = downOne(seq)
				childValues.append(data[0])
				seq = data[1]

		if nChild == 0:
			for _ in range(nMetric):
				mSum += seq.pop(0)
			return(mSum, seq)
		else:
			for _ in range(nMetric):
				if seq[0] > nChild:
					mSum += 0
					_ = seq.pop(0)
				else:
					mSum += childValues[seq.pop(0)-1]
			return(mSum, seq)
	return(mSum, seq)

print(downOne(seq)[0])
