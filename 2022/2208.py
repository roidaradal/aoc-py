# Advent of Code 2022 Day 08
# John Roy Daradal 

from aoc import *

def data(full: bool) -> IntGrid:
    return [toIntLine(line) for line in readLines(22, 8, full)]

def solve():
    grid = data(full=True)
    rows,cols = getBounds(grid)

    visible: set[coords] = set()
    maxScore = 0
    for row in range(1,rows-1):
        for col in range(1,cols-1):
            checkRowVisible(grid, visible, (row,col))
            checkColVisible(grid, visible, (row,col))
            maxScore = max(maxScore, computeScore(grid, row, col))
    numEdges = (2 * cols) + (2 * (rows-2))
    count = numEdges + len(visible)
    print(count)
    print(maxScore)

def checkRowVisible(grid: IntGrid, visible: set[coords], c: coords):
    if c in visible: return 
    row,col = c 
    isLower = lambda x: x < grid[row][col]
    if all(isLower(x) for x in grid[row][:col]): # visible from left
        visible.add(c)
        return 
    if all(isLower(x) for x in grid[row][col+1:]): # visible from right
        visible.add(c)

def checkColVisible(grid: IntGrid, visible: set[coords], c: coords):
    if c in visible: return 
    row,col = c 
    isLower = lambda x: x < grid[row][col]
    above = [grid[r][col] for r in range(0,row)]
    if all(isLower(x) for x in above):
        visible.add(c)
        return 
    below = [grid[r][col] for r in range(row+1,len(grid))]
    if all(isLower(x) for x in below):
        visible.add(c)

def computeScore(grid: IntGrid, row: int, col: int) -> int:
    rows,cols = getBounds(grid)
    value = grid[row][col]
    n, e, w, s, = 0, 0, 0, 0 
    # Up 
    for r in range(row-1,-1,-1):
        n += 1
        if grid[r][col] >= value: break 
    # Down 
    for r in range(row+1, rows):
        s += 1
        if grid[r][col] >= value: break
    # Left 
    for c in range(col-1,-1,-1):
        w += 1
        if grid[row][c] >= value: break 
    # Right 
    for c in range(col+1, cols):
        e += 1
        if grid[row][c] >= value: break 

    return n*e*w*s

if __name__ == '__main__':
    do(solve)

'''
Part 1: 
- Go through each inner cell (exclude edge cells)
- Check if cell is visible from left/right or from above/below
- CheckRowVisible: check if all cells to the left / right are all lower than current cell
- CheckColVisible: check if all cells above / below are all lower than current cell
- Total visible = count of visible inner cells + count edge cells (all visible)

Part 2:
- Go through each inner cell and compute their score 
- Count the number of visible trees above, below, left, and right 
- If view is already blocked, stop counting in that direction 
- Score = product of counts above, below, left, right
- Output the maximum score
'''