#!/usr/bin/env python3.10

from collections import Counter, OrderedDict

card_order = [
    "A", "K", "Q", "T", "9", "8",
    "7", "6", "5", "4", "3", "2", "J"
]
hand_group_order = [
    "five_of_a_kind",
    "four_of_a_kind",
    "full_house",
    "three_of_a_kind",
    "two_pair",
    "one_pair",
    "high_card"
]

hand_groups = {
    hand_group: {}
    for hand_group in hand_group_order
}


def get_sort_order(hand: str) -> tuple[int]:
    return tuple(card_order.index(card) for card in hand)


lines = open("input.txt").readlines()
n_hands = len(lines)
for line in open("input.txt").readlines():
    hand, bid = line.strip().split()
    bid = int(bid)
    count_cards = Counter(hand)

    # Treat J as wildcard that makes best hand
    match sorted(count_cards.values()):
        case [5]:
            group = "five_of_a_kind"
        case [1, 4]:
            group = "four_of_a_kind"
            if 'J' in hand:
                group = "five_of_a_kind"
        case [2, 3]:
            group = "full_house"
            if 'J' in hand:
                group = "five_of_a_kind"
        case [1, 1, 3]:
            group = "three_of_a_kind"
            if 'J' in hand:
                group = "four_of_a_kind"
        case [1, 2, 2]:
            group = "two_pair"
            if 'J' in hand:
                if count_cards['J'] == 2:
                    group = "four_of_a_kind"
                else:
                    group = "full_house"
        case [1, 1, 1, 2]:
            group = "one_pair"
            if 'J' in hand:
                group = "three_of_a_kind"
        case [1, 1, 1, 1, 1]:
            group = "high_card"
            if 'J' in hand:
                group = "one_pair"
        case _:
            raise ValueError("Unexpected hand type")

    hand_groups[group][get_sort_order(hand)] = (hand, bid)


total = 0
index = n_hands
for hand_group in hand_group_order:
    group = hand_groups[hand_group]
    if len(group) == 1:
        key = list(group.keys())[0]
        hand, bid = group[key]
        total += (index) * bid
        print(f"{hand=} {key=} {bid=} {index=} value={bid * index} {total=}")
        index -= 1
    else:
        keys_sorted = sorted(group.keys())
        for key in keys_sorted:
            hand, bid = group[key]
            total += (index) * bid
            print(f"{hand=} {key=} {bid=} {index=} value={bid * index} {total=}")
            index -= 1

print(total)
