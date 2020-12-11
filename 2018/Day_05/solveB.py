#!/usr/bin/env python3

import os
import string


# Base clash finding function
def check_clash(char_a, char_b):
	if char_a.lower() != char_b.lower():
		return False
	elif char_a.isupper() + char_b.isupper() != 1:
		return False
	else:
		return True


def read_file(filename):
	if not os.path.isfile(filename):
		print('Invalid file')
		return
	else:
		lines = open(filename).readlines()
		if len(lines) == 1:
			return lines[0].strip()
		else:
			print('Multiple lines found in input file')
			return


# Remove specific bases
def remove_base(seq, base):
	return seq.replace(base.lower(), '').replace(base.upper(), '')


# Scan sequence for clashing pairs, only keep non-clashes, rescan until none are found
def scan_seq(seq):
	no_changes = False
	previous_clashed = False

	while not no_changes:
		seq2 = ''
		for i in range(len(seq)):
			# This prevents 'cCc'-like motifs being fully excluded
			if previous_clashed:
				previous_clashed = False
				continue
			# Perform forward check, unless at the end of the sequence
			if i+1 <= len(seq)-1 and check_clash(seq[i], seq[i+1]):
				previous_clashed = True
				continue
			# Add 0-base if no clash was found
			else:
				previous_clashed = False
				seq2 += seq[i]
		# Check if sequence length has changed, set leave bool if it hasn't
		if len(seq) == len(seq2):
			no_changes = True
		seq = seq2

	return len(seq)


# Find shortest possible sequence, given base removal
minLen = float("inf")
file_seq = read_file('input.txt')
for base_lc in string.ascii_lowercase:
	seqLen = scan_seq(remove_base(file_seq, base_lc))
	if seqLen < minLen:
		minLen = seqLen
		baseRemoved = base_lc
print(minLen)
