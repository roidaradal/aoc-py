# Advent of Code 2023 Day 06
# John Roy Daradal 

from aoc import *

def data(full: bool) -> tuple[list[int], list[int]]:
    numbers = []
    for line in readLines(23, 6, full):
        numbers.append([int(x) for x in line.split()[1:]])
    times, bests = numbers 
    return times, bests

def solve():
    times, bests = data(full=True)

    # Part 1
    total = 1
    for i,limit in enumerate(times):
        breakers = sum(1 for d in computeOutcomes(limit) if d > bests[i])
        total *= breakers
    print(total)

    # Part 2
    limit = int(''.join(str(x) for x in times))
    best  = int(''.join(str(x) for x in bests))
    breakers = sum(1 for d in computeOutcomes(limit) if d > best)
    print(breakers)

def computeOutcomes(limit: int) -> list[int]:
    return [hold * (limit-hold) for hold in range(limit+1)]

if __name__ == '__main__':
    do(solve)

'''
Solve:
- For a given time limit, calculate the outcomes if we hold for 0, 1, ..., limit seconds
- The speed is the number of seconds we hold, and it will travel at that speed for the remaining time (limit-hold)
- From the outcomes, only consider distances that will beat the current best
- For Part 1, solve for each limit-best pair and get the product of the number of record-breakers
- For Part 2, concatenate the digits to form one limit-best pair
'''