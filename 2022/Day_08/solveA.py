#!/usr/bin/env python3


def collect_visible(trees: list, i_range: list, j_range: list, top_bot: bool = True) -> set:
	visible = set()

	for i in i_range:
		highest = -1
		for j in j_range:
			x, y = (j, i) if top_bot else (i, j)

			tree = int(trees[x][y])
			if tree > highest:
				highest = tree
				visible.add((x, y))
			if tree == 9:
				break

	return visible


def scan_trees(filename: str) -> set:
	trees = [line.strip() for line in open(filename).readlines()]

	height = len(trees)
	width = len(trees[0])

	visible = set()
	visible_top_bot = collect_visible(trees, range(width), range(height))
	visible_bot_top = collect_visible(trees, range(width), range(height)[::-1])
	visible_left_right = collect_visible(trees, range(width), range(height), top_bot=False)
	visible_right_left = collect_visible(trees, range(width), range(height)[::-1], top_bot=False)

	visible = visible_top_bot | visible_bot_top | visible_left_right | visible_right_left

	return visible


if __name__ == '__main__':
	assert scan_trees("test.txt") == {
		(0,0), (1,0), (2,0), (3,0), (4,0),
		(0,1), (1,1), (2,1),        (4,1),
		(0,2), (1,2),        (3,2), (4,2),
		(0,3),        (2,3),        (4,3),
		(0,4), (1,4), (2,4), (3,4), (4,4),
	}

	print(len(scan_trees('input.txt')))
