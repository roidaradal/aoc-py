# Advent of Code 2018 Day 18
# John Roy Daradal 

from aoc import *

Grid = list[str]

def data(full: bool) -> Grid:
    return readLines(18, 18, full)

def solve() -> Solution:
    grid = data(full=True)
    cols = getBounds(grid)[1]

    results: list[str] = []
    results.append(gridState(grid))
    idx: int = 0 
    loopLength: int = 0 
    while True:
        grid = nextGrid(grid)

        state = gridState(grid)
        if state in results:
            idx = results.index(state)
            loopLength = len(results) - idx 
            break
        results.append(state)

    # Part 1 
    state1 = results[10]
    grid1 = gridFromState(state1, cols)
    value1 = resourceValue(grid1)

    cycles = 1_000_000_000 
    cycles = cycles - idx 
    loopIdx = cycles % loopLength 
    state2 = results[idx + loopIdx]
    grid2 = gridFromState(state2, cols)
    value2 = resourceValue(grid2)

    return newSolution(value1, value2)

def resourceValue(grid: Grid) -> int:
    tree, lumber = 0, 0 
    for line in grid:
        for char in line:
            if char == '|':
                tree += 1 
            elif char == '#':
                lumber += 1
    return tree * lumber

def gridState(grid: Grid) -> str:
    return ''.join(''.join(line) for line in grid)

def gridFromState(state: str, cols: int) -> Grid:
    grid: Grid = []
    for x in range(0, len(state), cols):
        grid.append(state[x:x+cols])
    return grid

def nextGrid(grid: Grid) -> Grid:
    bounds = getBounds(grid)
    rows,cols = bounds
    grid2: Grid = []
    for row in range(rows):
        line2: list[str] = []
        for col in range(cols):
            line2.append(nextState(grid, bounds, (row,col)))
        grid2.append(''.join(line2))
    return grid2

OPEN, TREE, LUMBER = '.', '|', '#'
def nextState(grid: Grid, bounds: dims2, curr: coords) -> str:
    near = [grid[ny][nx] for ny,nx in surround8(curr) if insideBounds((ny,nx), bounds)]
    y,x = curr 
    tile = grid[y][x]
    if tile == OPEN:
        nearTree = near.count(TREE)
        return TREE if nearTree >= 3 else OPEN 
    elif tile == TREE: 
        nearLumber = near.count(LUMBER)
        return LUMBER if nearLumber >= 3 else TREE
    else: # LUMBER 
        nearLumber = near.count(LUMBER)
        nearTree = near.count(TREE)
        return LUMBER if nearLumber >= 1 and nearTree >= 1 else OPEN

if __name__ == '__main__':
    do(solve, 18, 18)

'''
Solve:
- Repeatedly compute the next grid; remember the state of the grid after each minute 
- Next grid computes the next tiles based on the current tile and neighbors:
    - Get the tile types of surround8 neighbors that are within grid bounds 
    - If OPEN tile, change to TREE if nearTree >= 3 
    - If TREE tile, change to LUMBER if nearLumber >= 3 
    - If LUMBER tile, keep LUMBER if nearLumber >=1 and nearTree >= 1, else change to OPEN
- Stop if we have reached a state that has already been seen before (loop detected)
- Compute the state at the 1 billionth minute, similar to AOC 2314
- For Part 1, output the resource value of grid at 10th minute 
- For Part 2, output the resource value of grid at 1Bth minute
- Resource value is the product of tree count and lumber count in the grid
'''


