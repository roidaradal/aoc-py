# Advent of Code 2023 Day 21
# John Roy Daradal 

from aoc import *
from collections import deque 
import numpy as np

Grid = list[str]

def data(full: bool) -> tuple[Grid, coords]:
    grid = readLines(23, 21, full)
    start: coords = (0,0)
    for row,line in enumerate(grid):
        replace = False
        for col,tile in enumerate(line):
            if tile == 'S':
                start = (row,col)
                replace = True 
        if replace: grid[row] = line.replace('S', '.')
    return grid, start

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    grid, start = data(full=True)
    bounds = getBounds(grid)
    current: set[coords] = set([start])
    for _ in range(64):
        current2: set[coords] = set()
        for curr in current:
            for nxt in surround4(curr):
                ny,nx = nxt 
                if not insideBounds(nxt, bounds): continue 
                if grid[ny][nx] == '#': continue 
                current2.add(nxt)
        current = current2

    return len(current)

def part2() -> int:
    grid, start = data(full=True)
    rows, cols = getBounds(grid)
    finalX, remainder = divmod(26_501_365, cols)
    crossings = [remainder, remainder + cols, remainder + (2*cols)]

    visited = set()
    deq = deque([start])
    total = [0, 0] # even, odd
    Y = []
    for step in range(1, crossings[-1]+1):
        for _ in range(len(deq)):
            x, y = deq.popleft()
            for i,j in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if (i,j) in visited or grid[i%rows][j%cols] == '#':
                    continue 

                visited.add((i,j))
                deq.append((i,j))
                total[step % 2] += 1
        
        if step in crossings:
            Y.append(total[step%2])
    
    X = [0,1,2]
    coeff = np.polyfit(X, Y, deg=2) # get coeff for quadratic equation y = ax^2 + bx + c 
    finalY = np.polyval(coeff, finalX)
    count = int(str(finalY.round().astype(int)))
    return count

if __name__ == '__main__':
    do(solve, 23, 21)

'''
Part1:
- Start with current point at start (center)
- At each step, move the current points to their 4 neighbors as long as it doesn't 
  go out of bounds and there is no wall in the next position
- Use a set for the points to avoid duplication
- Repeat for 64 steps and output the final number of current points

Part2:
- Burnout, used a Reddit solution to complete Aoc 2023
- Reference: https://github.com/mgtezak/Advent_of_Code/blob/master/2023/Day_21.py
'''