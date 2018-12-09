# Parse input data
inFile = open('inputA.txt').read().split(' ')
n_players, top_marble = int(inFile[0]), int(inFile[6])

# Initiate values
play_state = [0]
marble = 1
scores = {}
player = 1
ins_point = 0

# Play game
while marble <= top_marble:
	if marble % 23 == 0:
		# Apply weird marble rule
		ins_point = (ins_point-7) if (ins_point >= 7) else len(play_state)-7+ins_point
		if player not in scores.keys():
			scores[player] = marble + play_state.pop(ins_point)
		else:
			scores[player] += marble + play_state.pop(ins_point)
	else:
		# Apply standard insertion rule
		ins_point = (ins_point+2 - len(play_state)) if (ins_point+2 > len(play_state)) else ins_point+2
		play_state.insert(ins_point, marble)
		curr_marble = play_state.index(marble)

	# Move to next marble & player
	marble += 1
	player = player+1 if player <= n_players-1 else 1

max_score = max(scores.values())
winner = max(scores, key=scores.get)

print(f'{winner} wins with a score of {max_score}')