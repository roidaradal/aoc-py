# Advent of Code 2021 Day 01
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int]:
    return [int(line) for line in readLines(21, 1, full)]

def solve() -> Solution:
    numbers = data(full=True)

    # Part 1
    fn1 = lambda i: numbers[i+1] > numbers[i]
    indexes = list(range(len(numbers)-1))
    count1 = countValid(indexes, fn1)

    # Part 2 
    fn2 = lambda i: sum(numbers[i-2:i+1]) > sum(numbers[i-3:i])
    indexes = list(range(3, len(numbers)))
    count2 = countValid(indexes, fn2)

    return newSolution(count1, count2)

if __name__ == '__main__':
    do(solve, 21, 1)

'''
Part1:
- Count valid numbers: valid if greater than previous number

Part2:
- Count valid numbers: process in windows of 3 
- Valid if sum of current 3-window is greater than previous 3-window
'''