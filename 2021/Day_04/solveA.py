#!/usr/bin/env python3

import pandas as pd
import numpy as np

from dataclasses import dataclass


@dataclass
class BingoBoard:
	board: pd.DataFrame = pd.DataFrame()  # Holds bingo values
	winning: bool = False

	def add_row(self, values: list):
		self.board[self.board.shape[1]] = values

	def view_board(self):
		for row in self.board:
			print(' '.join(row))

	def update_board(self, value: int):
		coords = tuple(zip(*np.where(self.board == value)))
		self.board.replace({value: np.NaN}, inplace=True)
		for row, col in coords:
			self.check_if_won(col, row)
			if self.winning == True:
				return True
		return False

	def check_if_won(self, column, row):
		checks = {
			len(self.board[column].values[~np.isnan(self.board[column].values)]),
			len(self.board.iloc[row].values[~np.isnan(self.board.iloc[row].values)])
		}
		if 0 in checks:
			self.winning = True

	def total(self) -> int:
		return self.board.sum().sum()


# Play bingo
def play_bingo(balls, boards):
	for ball in balls:
		for board in boards:
			if board.update_board(ball):
				board_total = board.total()
				score = int(board_total * ball)
				print(score)
				return
	else:
		return "No win"


# Read input file
with open('input.txt','r') as f:
	balls = map(int, f.readline().split(','))

	boards = []
	for line in f.readlines():
		if line == '\n':
			boards.append(BingoBoard(pd.DataFrame()))
		else:
			boards[-1].add_row(list(map(int, line.rstrip().split())))

play_bingo(balls, boards)
