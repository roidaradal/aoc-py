# Advent of Code 2021 Day 25
# John Roy Daradal 

from aoc import *

Grid = list[list[str]]

def data(full: bool) -> Grid:
    return [list(line) for line in readLines(21, 25, full)]

def solve() -> Solution:
    grid = data(full=True)
    bounds = getBounds(grid)

    steps = 0
    while True:
        grid, count1 = moveHerd(grid, R, bounds)
        grid, count2 = moveHerd(grid, D, bounds)
        steps += 1 
        if count1 + count2 == 0: break 

    return newSolution(steps, "")

def moveHerd(grid: Grid, d: delta, bounds: dims2) -> tuple[Grid, int]:
    target = 'v' if d == D else '>'
    free = '.'
    count = 0 
    grid2: Grid = [line[:] for line in grid] # copy previous grid
    for y,line in enumerate(grid):
        for x,tile in enumerate(line):
            if tile != target: continue
            ny,nx = nextOf((y,x), d, bounds)
            if grid[ny][nx] == free:
                grid2[y][x] = free
                grid2[ny][nx] = target
                count += 1
    return grid2, count

def nextOf(c: coords, d: delta, bounds: dims2) -> coords:
    rows,cols = bounds
    ny,nx = move(c, d)
    if d == D and ny == rows:
        return (0, nx) # wrap around to first row 
    elif d == R and nx == cols:
        return (ny, 0) # wrap around to first col
    else:
        return (ny,nx)

if __name__ == '__main__':
    do(solve, 21, 25)

'''
Solve:
- Repeat until there is no more movement after that step (deadlock)
    - Move all east-facing sea cucumbers that can move 
    - Move all south-facing sea cucumbers that can move
- When moving a herd of sea cucumbers, we update the grid and count the number of movement
    - Create a copy of the previous grid (this is what we will update)
    - Focus on the tiles that are part of the herd (v for south, > for east)
    - Check if the next tile (with wrap-around to the front if exceeds grid bounds) is empty
    - If empty, we can move the sea cucumber forward
- Output the number of steps it took to reach deadlock
- No problem for Part 2
'''