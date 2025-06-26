# Advent of Code 2015 Day 18
# John Roy Daradal 

from aoc import *

LightGrid = list[list[bool]]

def data(full: bool) -> LightGrid:
    def fn(line: str) -> list[bool]:
        return [x == '#' for x in line]
    return [fn(line) for line in readLines(15, 18, full)]

def solve() -> Solution:
    # Part 1
    grid = data(full=True)
    for _ in range(100):
        grid = nextGrid(grid, False)
    total1 = sum(sum(line) for line in grid)

    # Part 2 
    grid = data(full=True)
    bounds = getBounds(grid)
    for y,x in getCorners(bounds):
        grid[y][x] = True 
    for _ in range(100):
        grid = nextGrid(grid, True)
    total2 = sum(sum(line) for line in grid)

    return newSolution(total1, total2)

def nextGrid(grid: LightGrid, onCorners: bool) -> LightGrid:
    rows, cols = getBounds(grid)
    grid2: LightGrid = []
    for row in range(rows):
        line = [nextState((row,col), grid, onCorners) for col in range(cols)]
        grid2.append(line)
    return grid2

def nextState(center: coords, grid: LightGrid, onCorners: bool) -> bool:
    bounds = getBounds(grid)
    if onCorners and center in getCorners(bounds):
        return True
    
    y,x = center 
    on = grid[y][x] 
    near = [nxt for nxt in surround8(center) if insideBounds(nxt, bounds)]
    nearCount = sum(grid[y][x] for y,x in near)
    if on:
        return nearCount == 2 or nearCount == 3
    else:
        return nearCount == 3

def getCorners(bounds: dims2) -> list[coords]:
    rows, cols = bounds 
    return [(0,0), (0,cols-1), (rows-1,0), (rows-1,cols-1)]

if __name__ == '__main__':
    do(solve, 15, 18)

'''
- For Part 1, transform the grid 100 times, and count the number of turned on lights
- For Part 2, turn on the corner lights, then transform 100 times while keeping the corners on 
- To transform the light grid, simultaneously change all cells by checking next state:
    - If Part 2 (onCorners) and cell is corner cell, turn on 
    - Check the surrounding 8 cells that are within bounds 
    - Count the number of turned on lights from the valid neighbors 
    - If light is currently on, remain on if nearCount is 2 or 3 
    - If light is off, turn on if nearCount is 3
'''