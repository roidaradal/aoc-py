# Advent of Code 2015 Day 17
# John Roy Daradal 

import itertools
from aoc import *

def data(full: bool) -> list[int]:
    return [int(line) for line in readLines(15, 17, full)]

def solve() -> Solution:
    numbers = data(full=True)

    total1, total2 = 0, 0
    for i in range(2, len(numbers)):
        count = 0
        for combo in itertools.combinations(numbers, i):
            if sum(combo) == 150:
                count += 1

        # Part 1 
        total1 += count 

        # Part 2
        if total2 == 0 and count > 0:
            total2 = count

    return newSolution(total1, total2)


if __name__ == '__main__':
    do(solve, 15, 17)

'''
Solve:
- Go through combo length options from 2 to len(numbers) 
- Go through the combinations of numbers for this combo length 
- If the combo sum == 150, increment count for this combo length 
- For Part 1, sum up the counts for all combo lengths 
- For Part 2, find the minimum combo length that has valid combos, output its count
'''