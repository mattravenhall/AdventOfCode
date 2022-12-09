#!/usr/bin/env python3


def count_visible(trees: list, height: int) -> int:
	visible = 0
	for tree in trees:
		visible += 1
		if int(tree) >= height:
			break
	return visible


def find_scenic(filename: str) -> int:
	trees = [line.strip() for line in open(filename).readlines()]

	height = len(trees)
	width = len(trees[0])

	most_scenic = -1
	for y in range(height):
		for x in range(width):
			tree = int(trees[y][x])

			view_top = [row[x] for row in trees[:y]][::-1]
			view_bot = [row[x] for row in trees[y+1:]]
			view_left = trees[y][:x][::-1]
			view_right = trees[y][x+1:]

			visible_top = count_visible(view_top, height=tree)
			visible_bot = count_visible(view_bot, height=tree)
			visible_left = count_visible(view_left, height=tree)
			visible_right = count_visible(view_right, height=tree)

			scenic_score = visible_top * visible_bot * visible_left * visible_right

			if scenic_score > most_scenic:
				most_scenic = scenic_score
	
	return most_scenic


if __name__ == '__main__':
	assert find_scenic("test.txt") == 8

	print(find_scenic('input.txt'))
