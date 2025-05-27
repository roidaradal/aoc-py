# Advent of Code 2021 Day 09
# John Roy Daradal 

from aoc import *

Grid = list[list[int]]

def data(full: bool) -> Grid:
    def fn(line: str) -> list[int]:
        return [int(x) for x in line]
    return [fn(line) for line in readLines(21, 9, full)]

def solve():
    grid = data(full=True)

    # Part 1
    low = findLowPoints(grid)
    total = sum(pt[2] + 1 for pt in low)
    print(total)

    # Part 2
    basins = [basinSize(grid, (y,x)) for y,x,_ in low]
    basins.sort(reverse=True)   # Get the 3 biggest basin sizes 
    b1,b2,b3 = basins[0:3]
    print(b1*b2*b3)


def findLowPoints(grid: Grid) -> list[int3]:
    low: list[int3] = []
    for row, line in enumerate(grid):
        for col, height in enumerate(line):
            near = surrounding(grid, (row,col))
            if all(h > height for _,_,h in near):
                low.append((row,col,height))
    return low

def surrounding(grid: Grid, center: coords) -> list[int3]:
    bounds = getBounds(grid)
    near = []
    for y,x in surround4(center):
        if not insideBounds((y,x), bounds): continue
        near.append((y,x,grid[y][x]))
    return near

def basinSize(grid: Grid, center: coords) -> int:
    visited = set()
    stack = [center]
    while len(stack) > 0:
        c = stack.pop()
        visited.add(c)
        for y,x,h in surrounding(grid, c):
            if (y,x) in visited or h == 9: continue 
            stack.append((y,x))
    return len(visited)

if __name__ == '__main__':
    do(solve)

'''
Part1:
- To find the low points in the grid, go through each cell 
- Get the 4 surrounding cells (NEWS) of current cell
- If all surrounding cells have higher height than current cell, it is a low point 
- Output the sum of low point's (height + 1)

Part2:
- For each low point in Part 1, find its basin size 
- Use depth-first search to flood-fill starting from the low point
- Expansion in a direction stops when we find a cell of height 9 (or out of bounds)
- Low point's basin size is the number of visited cells from the flood-fill
- Get the 3 biggest basin sizes and output their product
'''