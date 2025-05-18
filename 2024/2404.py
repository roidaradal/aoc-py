# Advent of Code 2024 Day 04
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[str]:
    return readLines(24, 4, full)

def part1():
    grid = data(full=True)
    # Find starting X
    points = [(r,c) for r,line in enumerate(grid) for c,char in enumerate(line) if char == 'X']
    bounds = getBounds(grid)
    vectors = []
    # Find next M from X's neighbors
    for center in points: 
        for pt in surround8(center):
            if not insideBounds(pt, bounds): continue 
            row, col = pt 
            if grid[row][col] == 'M':
                vectors.append((pt, getDelta(center, pt)))
    # Complete A, S
    for letter in 'AS':
        vectors = findNextPositions(grid, vectors, letter)
    print(len(vectors))

def part2():
    grid = data(full=True)
    # Find middle A
    rows,cols = getBounds(grid)
    points = []
    for row, line in enumerate(grid):
        for col, char in enumerate(line):
            if char == 'A' and insideBounds((row,col), (rows-1,cols-1),(1,1)):
                points.append((row,col))
    # Find X-MAS
    xmas = []
    for row,col in points:
        # Left diagonal 
        tl = grid[row-1][col-1]
        br = grid[row+1][col+1]
        ldiag = tl + 'A' + br
        # Right diagonal 
        tr = grid[row-1][col+1]
        bl = grid[row+1][col-1]
        rdiag = tr + 'A' + bl 
        if isXMAS(ldiag, rdiag): 
            xmas.append((row,col))
    print(len(xmas))
     
def findNextPositions(grid: list[str], vectors: list[vector], letter: str) -> list[vector]:
    bounds = getBounds(grid)
    vectors2 = []
    for c,d in vectors:
        c = move(c, d)
        if not insideBounds(c, bounds): continue 
        row, col = c 
        if grid[row][col] == letter:
            vectors2.append((c,d))
    return vectors2

def isXMAS(diag1: str, diag2: str) -> bool:
    return all(d in ('MAS','SAM') for d in (diag1, diag2))

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Find all coords for X 
- For each X coord, find M in its neighbors
- Take note of the coords and delta of the neighbor (need to keep going in that direction)
- For A and S, find the next positions by finding the neighbor letter from previous vectors
- Keeping the delta direction, check if there is a letter of interest in that direction

Part2:
- Start by finding all coords of A that are inside the inner bounds: (1,1) to (rows-1,cols-1)
- Use inner bounds so we are sure that it can have a diagonal using one level above and below
- From the center A coords, check the left diagonal and right diagonal
- Check if both diagonals form a MAS or SAM
'''