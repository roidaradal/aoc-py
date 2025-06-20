# Advent of Code 2020 Day 03
# John Roy Daradal 

import math
from aoc import *

def data(full: bool, d: delta) -> list[str]:
    lines = readLines(20, 3, full)
    dy, dx = d 
    h, w = len(lines), len(lines[0])
    needW = (1 + dx) * numSteps(h, dy) 
    repeat = math.ceil(needW / w)
    return [line * repeat for line in lines]

def solve() -> Solution:
    # Part 1
    count = countSlope((1,3), full=True)
    
    # Part 2
    product = 1 
    for d in [(1,1), (1,3), (1,5), (1,7), (2,1)]:
        product *= countSlope(d, full=True)

    return newSolution(count, product)

def numSteps(height: int, dy: int) -> int:
    return (height-1) // dy

def countSlope(d: delta, full: bool) -> int:
    curr = (0,0)
    g = data(full, d)
    count = 0
    height, dy = len(g), d[0]
    for _ in range(numSteps(height, dy)):
        curr = move(curr, d)
        row, col = curr 
        if g[row][col] == '#':
            count += 1
    return count

if __name__ == '__main__':
    do(solve, 20, 3)

'''
Data:
- Determine the number of times the input will be repeated horizontally 
- numSteps to finish is height-1 (because we start at first row) / deltaY
    - example: if height is 10 and dy=3, numSteps = 3
- Compute the needed width to finish the steps: (deltaX + 1) * numSteps (add 1 for margin)
- Repeat = ceil(needW / actual width), e.g. needW = 15, actualW = 10, repeat = 2

Part1:
- Repeat numSteps times, use delta = (1,3)
    - repeatedly move through grid using delta 
    - if you encounter a '#' at each step, increase count

Part2:
- Repeat Part1 but with different deltas 
- Get the product of the results of using each delta
'''