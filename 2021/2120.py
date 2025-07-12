# Advent of Code 2021 Day 20
# John Roy Daradal 

from aoc import *

Grid = dict[coords, int]

def data(full: bool) -> tuple[list[int], Grid]:
    lines = readLines(21, 20, full)
    lookup = [1 if x == '#' else 0 for x in lines[0]]
    grid: Grid = {}
    for row, line in enumerate(lines[2:]):
        for col, char in enumerate(line):
            grid[(row,col)] = 1 if char == '#' else 0
    return lookup, grid

def solve() -> Solution:
    # Part 1
    count1 = countAfterRounds(2)
    
    # Part 2
    count2 = countAfterRounds(50)

    return newSolution(count1, count2)

def countAfterRounds(rounds: int) -> int:
    lookup, grid = data(full=True)
    for i in range(rounds):
        default = 0 if i % 2 == 0 else 1
        grid = nextGrid(grid, lookup, default)
    return countOn(grid)

def countOn(grid: Grid) -> int:
    count = 0
    for bit in grid.values():
        if bit == 1: count += 1
    return count

def nextGrid(grid: Grid, lookup: list[int], default: int) -> Grid:
    ys = set([c[0] for c in grid.keys()])
    xs = set([c[1] for c in grid.keys()])
    x1 = min(xs) - 2 
    x2 = max(xs) + 3 
    y1 = min(ys) - 2 
    y2 = max(ys) + 3 
    grid2: Grid = {}
    for y in range(y1, y2):
        for x in range(x1, x2):
            neighbor = surround8((y,x))
            pos = neighbor[0:3] + [neighbor[3], (y,x), neighbor[4]] + neighbor[5:8]
            bits = ''.join(str(grid.get(c, default)) for c in pos)
            idx = int(bits, 2)
            grid2[(y,x)] = lookup[idx]
    return grid2

if __name__ == '__main__':
    do(solve, 21, 20)

'''
Solve:
- Use a regular dict, not a defaultdict, as we will be changing the default value 
  depending on whether the round is even or odd
- Checking the lookup line, 0 is translated to #, while 512 is translated to .
    - This means that if you currently have no neighbors, in the next round it will turn to #
    - On the other hand, if you're surrounded by #, in the next round you will turn back into .
    - So the infinite grid alternates from being all dots to being all #
    - So we feed a different default value depending on the round: 0 on even, 1 on odd
- For the number of rounds given, compute the next grid:
    - Since the grid is contained in a dict, find the min/max x and y values in the grid
    - Extend the min x/y by -2 (so that the prev min will become center)
    - Extend the max x/y by +2 (so that the prev max will become center)
    - For the new range of y, x, check each cell (y,x)
    - Get the 8 neighbors and combine it with the current cell to form 3 rows 
    - The 0/1 mapping of the line forms a binary number -> the decimal value becomes the index to the lookup
    - Get the resulting bit from the lookup
- For Part 1, count the number of 1s in the grid after 2 rounds 
- For Part 2, count the number of 1s in the grid after 50 rounds
'''