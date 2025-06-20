# Advent of Code 2024 Day 01
# John Roy Daradal 

from aoc import *

def data(full: bool) -> tuple[list[int], list[int]]:
    col1, col2 = [], []
    for line in readLines(24, 1, full):
        a, b = toIntList(line, None)
        col1.append(a)
        col2.append(b)
    return col1, col2

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    col1, col2 = data(full=True)
    col1.sort()
    col2.sort()
    diff = lambda x: abs(x[0]-x[1])
    cols = list(zip(col1,col2))
    return getTotal(cols, diff)

def part2() -> int:
    col1, col2 = data(full=True)
    freq = countFreq(col2)
    score = lambda x: x * freq[x]
    return getTotal(col1, score)

if __name__ == '__main__':
    do(solve, 24, 1)

'''
Part1:
- Sort the two columns in ascending order
- Zip the two columns to process the pairs together 
- Get the absolute difference of the pairs, and get the total

Part2:
- Count the frequency of column2 items 
- Score of items in column1 is the number * frequency in column2 
'''