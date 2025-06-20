# Advent of Code 2021 Day 07
# John Roy Daradal 

import sys
from aoc import *

def data(full: bool) -> list[int]:
    line = readFirstLine(21, 7, full)
    return toIntList(line, ',')

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    numbers = data(full=True)
    numbers.sort()
    median = numbers[len(numbers)//2]
    total = sum(abs(median-x) for x in numbers)
    return total

def part2() -> int:
    numbers = data(full=True)
    start, end = min(numbers), max(numbers)
    minCost = sys.maxsize
    for target in range(start, end+1):
        total = sum(sumRange(abs(target-x)) for x in numbers)
        minCost = min(minCost, total)
    return minCost
    
def sumRange(x: int) -> int:
    return sum(range(x+1))

if __name__ == '__main__':
    do(solve, 21, 7)

'''
Part1:
- Best position to align the crabs that will use the least total fuel if fuel cost is constant (1) is the median 
- Sort the positions and get the median (middle)
- Sum up the amount of fuel needed by each crab to move to the median

Part2:
- The best position to align the crabs if fuel cost is linear (step number = fuel) is somewhere between the min and max positions
- Go through each position in this range (even if there are no crabs currently in this position)
- Compute the cost of moving each crab to the current position
- Movement distance = abs(target-crab), but total fuel = sum from 1 to distance, because fuel cost is linear 
- Output the min cost found after checking all positions in the range
'''