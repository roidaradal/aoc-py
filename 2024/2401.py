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

def part1():
    col1, col2 = data(full=True)
    col1.sort()
    col2.sort()
    diff = lambda x: abs(x[0]-x[1])
    cols = list(zip(col1,col2))
    total = getTotal(cols, diff)
    print(total) 

def part2():
    col1, col2 = data(full=True)
    freq = countFreq(col2)
    score = lambda x: x * freq[x]
    total = getTotal(col1, score)
    print(total)

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Sort the two columns in ascending order
- Zip the two columns to process the pairs together 
- Get the absolute difference of the pairs, and get the total

Part2:
- Count the frequency of column2 items 
- Score of items in column1 is the number * frequency in column2 
'''