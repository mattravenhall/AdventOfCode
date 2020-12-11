import os

# Base clash finding function
def checkClash(charA, charB):
	if charA.lower() != charB.lower():
		return False
	elif charA.isupper() + charB.isupper() != 1:
		return False
	else:
		return True

def readFile(seq):
	if os.path.isfile(seq):
		lines = open(seq).readlines()
		if len(lines) == 1:
			return(lines[0].strip())
		else:
			print('Multiple lines found in input file')
			return

# Remove specific bases
def removeBase(seq, base):
	if os.path.isfile(seq):
		seq = readFile(seq)
	return(seq.replace(base.lower(),'').replace(base.upper(),''))

# Scan sequence for clashing pairs, only keep non-clashes, rescan until none are found
def scanSeq(seq):
	if os.path.isfile(seq):
		seq = readFile(seq)

	noChanges = False
	previousClashed = False

	while not noChanges:
		seq2 = ''
		for i in range(len(seq)):
			# This prevents 'cCc'-like motifs being fully excluded
			if previousClashed:
				previousClashed = False
				continue
			# Perform forward check, unless at the end of the sequence
			if i+1 <= len(seq)-1 and checkClash(seq[i], seq[i+1]):
				previousClashed = True
				continue
			# Add 0-base if no clash was found
			else:
				previousClashed = False
				seq2 += seq[i]
		# Check if sequence length has changed, set leave bool if it hasn't
		if len(seq) == len(seq2):
			noChanges = True
		seq = seq2

	return(len(seq))

# Find shortest possible sequence, given base removal
minLen = 9999999999999999999
for base in 'abcdefghijklmnopqrstuvwxyz':
	seqLen = scanSeq(removeBase('input.txt', base))
	if seqLen < minLen:
		minLen = seqLen
		baseRemoved = base
#	print('{0}: {1}'.format(base, seqLen))
print(minLen)
