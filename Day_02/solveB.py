lines = [line.strip() for line in open('input.txt') if line != '']
topMatch = [0 for x in range(len(lines[0]))]

for x in range(len(lines)-1):
	for y in range(len(lines)-1):
		if y <= x:
			continue
#		print(x, y)
#		print(lines[x], lines[y])

		matches = [lines[x][i] == lines[y][i] for i in range(len(lines[0]))]

		if sum(matches) > sum(topMatch):
			topMatch = matches
			topPair = [lines[x], lines[y]]

sharedLetters = ''.join([x for i, x in enumerate(topPair[0]) if topMatch[i]])

print(topPair)
print(sharedLetters)
