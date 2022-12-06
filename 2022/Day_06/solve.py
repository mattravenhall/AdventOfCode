#!/usr/bin/env python3


def parse(characters: str, marker_len: int = 4) -> int:
	# print(characters)
	for i in range(marker_len, len(characters)+1):
		marker = characters[i-marker_len: i]
		if len(set(marker)) == marker_len:
			break
	else:
		return None
	# print(f"{marker} ({i})")
	return i


if __name__ == '__main__':
	# Solve A
	assert parse("bvwbjplbgvbhsrlpgdmjqwftvncz", marker_len=4) == 5
	assert parse("nppdvjthqldpwncqszvftbrmjlhg", marker_len=4) == 6
	assert parse("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", marker_len=4) == 10
	assert parse("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", marker_len=4) == 11

	# Solve B
	assert parse("mjqjpqmgbljsphdztnvjfqwrcgsmlb", marker_len=14) == 19
	assert parse("bvwbjplbgvbhsrlpgdmjqwftvncz", marker_len=14) == 23
	assert parse("nppdvjthqldpwncqszvftbrmjlhg", marker_len=14) == 23
	assert parse("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", marker_len=14) == 29
	assert parse("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", marker_len=14) == 26

	characters = ''.join([line.strip() for line in open("input.txt").readlines()])
	print(f"A: {parse(characters, marker_len=4)}")
	print(f"B: {parse(characters, marker_len=14)}")
 