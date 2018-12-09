from blist import blist

# Parse input data
inFile = open('inputB.txt').read().split(' ')
n_players, top_marble = int(inFile[0]), int(inFile[6])

# Initiate values
play_state = blist([0])
marble = 1
scores = {}
ins_point = 0

# Play game
for marble in range(1,top_marble):
	if marble % 23 == 0:
		ins_point = (ins_point-7) if (ins_point >= 7) else len(play_state)-7+ins_point
		try:
			scores[marble % n_players] += marble + play_state.pop(ins_point)
		except:
			scores[marble % n_players] = marble + play_state.pop(ins_point)
	else:
		# Apply standard insertion rule
		ins_point = (ins_point+2) - (len(play_state) * int(ins_point+2 > len(play_state)))
		play_state.insert(ins_point, marble)
		curr_marble = ins_point

max_score = max(scores.values())
winner = max(scores, key=scores.get)

print(f'{winner} wins with a score of {max_score}')