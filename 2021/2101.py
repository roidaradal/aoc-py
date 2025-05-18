# Advent of Code 2021 Day 01
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int]:
    return [int(line) for line in readLines(21, 1, full)]

def part1():
    numbers = data(full=True)
    fn = lambda i: numbers[i+1] > numbers[i]
    indexes = list(range(len(numbers)-1))
    count = countValid(indexes, fn)
    print(count) 

def part2():
    numbers = data(full=True) 
    fn = lambda i: sum(numbers[i-2:i+1]) > sum(numbers[i-3:i])
    indexes = list(range(3, len(numbers)))
    count = countValid(indexes, fn)
    print(count) 

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Count valid numbers: valid if greater than previous number

Part2:
- Count valid numbers: process in windows of 3 
- Valid if sum of current 3-window is greater than previous 3-window
'''