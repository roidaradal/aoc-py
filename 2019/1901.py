# Advent of Code 2019 Day 01
# John Roy Daradal 

import math
from aoc import *

def data(full: bool) -> list[int]:
    return [int(line) for line in readLines(19, 1, full)]

def part1():
    numbers = data(full=True)
    total = getTotal(numbers, fuel)
    print(total) 

def part2():
    numbers = data(full=True)
    total = getTotal(numbers, totalFuel)
    print(total) 

def fuel(x: int) -> int: 
    return max(math.floor(x/3) - 2, 0)

def totalFuel(x: int) -> int: 
    total = 0 
    while x > 0:
        x = fuel(x)
        total += x 
    return total

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Compute total fuel needed by each module 
- fuel = floor(x/3) - 2; if negative, return 0

Part2:
- Compute recursive fuel needed by each number 
- While fuel needed is not 0, repeatedly compute fuel(x)
- Sum up total fuel as you reduce the number
'''