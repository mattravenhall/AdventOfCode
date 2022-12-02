#!/usr/bin/env python3

class RPS:
	opponent: dict = {
		"A": "Rock",
		"B": "Paper",
		"C": "Scissors",
	}

	player: dict = {
		"Rock": {
			"X": "Scissors",
			"Y": "Rock",
			"Z": "Paper",
		},
		"Paper": {
			"X": "Rock",
			"Y": "Paper",
			"Z": "Scissors",
		},
		"Scissors": {
			"X": "Paper",
			"Y": "Scissors",
			"Z": "Rock"
		}
	}

	points: dict = {
		"Rock": 1,
		"Paper": 2,
		"Scissors": 3,
	}

	outcomes: dict = {
		("Rock", "Rock"): 3,
		("Rock", "Paper"): 6,
		("Rock", "Scissors"): 0,
		("Paper", "Rock"): 0,
		("Paper", "Paper"): 3,
		("Paper", "Scissors"): 6,
		("Scissors", "Rock"): 6,
		("Scissors", "Paper"): 0,
		("Scissors", "Scissors"): 3,
	}

	def __init__(self, opponent_choice: str, player_choice: str):
		self.opponent_choice = self.opponent[opponent_choice]
		self.player_choice = self.player[self.opponent_choice][player_choice]

	def calc_score(self) -> int:
		score = self.points[self.player_choice] + self.outcomes[self.opponent_choice, self.player_choice]
		return score


if __name__ == '__main__':
	scores = [RPS(*line.split()).calc_score() for line in open("input.txt").readlines()]
	# print(scores)
	print(sum(scores))
