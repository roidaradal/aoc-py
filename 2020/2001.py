# Advent of Code 2020 Day 01
# John Roy Daradal 

import itertools
from aoc import *

def data(full: bool) -> list[int]:
    return [int(line) for line in readLines(20, 1, full)]

def solve() -> Solution:
    numbers = data(full=True)

    # Part 1
    value1 = find2020Combo(numbers, 2) 

    # Part 2 
    value2 = find2020Combo(numbers, 3)

    return newSolution(value1, value2)

def find2020Combo(numbers: list[int], count: int) -> int:
    for p in itertools.combinations(numbers, count):
        if sum(p) == 2020:
            prod = 1
            for x in p: prod *= x 
            return prod
    return 0

if __name__ == '__main__':
    do(solve, 20, 1)

'''
Find2020Combo:
- Go through each number combination of specified count 
- Find the combo that sums up to 2020 
- Return the product of the numbers in that combo
'''