# Advent of Code 2024 Day 02
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[list[int]]:
    fn = lambda line: toIntList(line, None)
    return [fn(line) for line in readLines(24, 2, full)]

def part1():
    numbersList = data(full=True)
    count = countValid(numbersList, isSafe)
    print(count) 

def part2():
    numbersList = data(full=True)
    count = countValid(numbersList, isSafe2)
    print(count) 

def isSafe(numbers: list[int]) -> bool:
    diffs = [numbers[i]-numbers[i-1] for i in range(1, len(numbers))]
    safeInc = all(1 <= d <= 3 for d in diffs)
    safeDec = all(-3 <= d <= -1 for d in diffs)
    return safeInc or safeDec

def isSafe2(numbers: list[int]) -> bool:
    remove = [None] + list(range(len(numbers)))
    for idx in remove:
        if idx is None:
            numbers2 = numbers[:]
        else:
            numbers2 = numbers[:idx] + numbers[idx+1:]
        if isSafe(numbers2):
            return True 
    return False

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Count safe numbers; get the differences between pairs 
- Check if all increasing (all positive) or all decreasing (all negative)
- Also ensure that diffs are within 1-3

Part2:
- Try removing each number (and also try removing nothing)
- Use the isSafe check in Part 1 for the updated numbers
'''