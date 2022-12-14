#!/usr/bin/env python3.10

from collections.abc import Iterable
from itertools import islice, zip_longest
import math


def compare_packages(left: list, right: list) -> bool:
    """Compare two given elements according to problem conditions"""
    match (left, right):
        case (int(), int()):
            if left == right:
                return None
            else:
                return left < right
        case (int(), list()):
            return compare_packages([left], right)
        case (list(), int()):
            return compare_packages(left, [right])
        case (list(), list()):
            for l, r in zip_longest(left, right):       
                if l is None:
                    return True
                if r is None:
                    return False

                comparison = compare_packages(l, r)
                if comparison is not None:
                    return comparison
            return None


def partition(array: list, index_low: int, index_high: int) -> int:
    """Find partition index for quicksort (using compare_packages not <)"""

    pivot = array[index_high]

    index_smaller = index_low - 1

    for index_loop in range(index_low, index_high):
        if compare_packages(array[index_loop], pivot):
            # If current element is correctly sorted, swap with i+1
            index_smaller += 1
            array[index_smaller], array[index_loop] = array[index_loop], array[index_smaller]

    # Swap pivot with greater element
    array[index_smaller+1], array[index_high] = array[index_high], array[index_smaller+1]

    # Return pivot index
    return index_smaller + 1


def quicksort(array: list, index_low: int = None, index_high: int = None) -> None:
    """Quick sort a given array in place"""

    # Default indexes are start and end
    if index_low is None:
        index_low = 0
    if index_high is None:
        index_high = len(array) - 1

    if index_low < index_high:
        # Find element where left values are lower than right
        pivot = partition(array, index_low, index_high)

        # Recurse into partitions
        quicksort(array, index_low, pivot - 1)
        quicksort(array, pivot + 1, index_high)


def solveA(filename: str, debug: bool = False) -> int:
    ordered = []
    with open(filename) as f:
        while True:
            parsed_group = list(islice(f, 3))
            if not parsed_group:
                break

            left, right = map(eval, parsed_group[:2])

            ordered.append(compare_packages(left, right))

    if debug:
        return ordered

    # Calculate sum of true indices
    return sum([i+1 for i, valid in enumerate(ordered) if valid])


def solveB(filename: str) -> int:
    packages = []
    dividers = [
        [[2]],
        [[6]]
    ]
    with open(filename) as f:
        while True:
            parsed_group = list(islice(f, 3))
            if not parsed_group:
                break
            left, right = map(eval, parsed_group[:2])
            packages.append(left)
            packages.append(right)
        
        # Insert divider packages
        for divider in dividers:
            packages.append(divider)

    # Quicksort packages in place
    quicksort(packages)

    # Determine decoder key
    decoder_key = math.prod([packages.index(divider)+1 for divider in dividers])
    return decoder_key


if __name__ == '__main__':
    assert solveA("test.txt", debug=True) == [True, True, False, True, False, True, False, False]
    assert solveA("test.txt") == 13
    print(f"A: {solveA('input.txt')}")

    assert solveB("test.txt") == 140
    print(f"B: {solveB('input.txt')}")
