# Advent of Code 2023 Day 14
# John Roy Daradal 

from aoc import *

Grid = list[list[str]]

def data(full: bool) -> Grid:
    return [list(line) for line in readLines(23, 14, full)]

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    grid = data(full=True)
    rollNorth(grid)
    return computeLoad(grid)

def part2() -> int:
    grid = data(full=True) 
    results: list[str] = []
    idx: int = 0
    loopLength: int = 0
    while True:
        rollNorth(grid)
        rollWest(grid)
        rollSouth(grid)
        rollEast(grid)

        state = gridState(grid)
        if state in results:
            idx = results.index(state)
            loopLength = len(results) - idx 
            break 
        results.append(state)

    cycles = 1_000_000_000
    cycles = (cycles-1) - idx # -1 for index mode, -idx to remove loop prefix
    loopIdx = cycles % loopLength 
    state = results[idx + loopIdx]
    cols = getBounds(grid)[1]
    grid = gridFromState(state, cols)
    return computeLoad(grid)

def computeLoad(grid: Grid) -> int:
    rows = getBounds(grid)[0]
    total = 0 
    for row, line in enumerate(grid):
        for char in line:
            if char != 'O': continue 
            total += rows - row
    return total 

def gridState(grid: Grid) -> str:
    return ''.join(''.join(line) for line in grid)

def gridFromState(state: str, cols: int) -> Grid:
    grid: Grid = []
    for x in range(0, len(state), cols):
        grid.append(list(state[x:x+cols]))
    return grid

def rollNorth(grid: Grid):
    rows = getBounds(grid)[0]
    for row in range(1, rows):
        line = grid[row]
        for col, char in enumerate(line):
            if char != 'O': continue 
            y = row-1
            while y >= 0:
                if grid[y][col] == '.':
                    grid[y][col] = 'O'
                    grid[y+1][col] = '.'
                    y -= 1
                else:
                    break

def rollSouth(grid: Grid):
    rows = getBounds(grid)[0]
    row = rows - 2 
    while row >= 0:
        line = grid[row]
        for col, char in enumerate(line):
            if char != 'O': continue 
            y = row+1 
            while y < rows:
                if grid[y][col] == '.':
                    grid[y][col] = 'O'
                    grid[y-1][col] = '.'
                    y += 1 
                else:
                    break 
        row -= 1

def rollWest(grid: Grid):
    rows, cols = getBounds(grid)
    for col in range(1, cols):
        for row in range(rows):
            if grid[row][col] != 'O': continue 
            x = col-1 
            while x >= 0:
                if grid[row][x] == '.':
                    grid[row][x] = 'O'
                    grid[row][x+1] = '.'
                    x -= 1
                else: 
                    break 

def rollEast(grid: Grid):
    rows, cols = getBounds(grid)
    col = cols - 2 
    while col >= 0:
        for row in range(rows):
            if grid[row][col] != 'O': continue 
            x = col+1 
            while x < cols:
                if grid[row][x] == '.':
                    grid[row][x] = 'O'
                    grid[row][x-1] = '.'
                    x += 1
                else:
                    break
        col -= 1

if __name__ == '__main__':
    do(solve, 23, 14)

'''
Solve: 
- For Part 1, roll the grid north once and compute the grid load 
- For Part 2, one cycle rolls the grid north, west, south, east 
- After each cycle, we cache the grid state to detect when we have looped back to a previous grid state
- After detecting the cycle, note the first time this state was detected (prefix) and the loop length (diff from now to first detection)
- To find the state at the 1billionth cycle, subtract 1 (for 0-based index) and the prefix index 
- The loop index from the cached states should be the (cycles % loopLength) + prefix index
- Rebuild the grid state from that index and compute the grid load
- The grid load is the total of (rows-row) of cells that have rocks (O)

RollNorth
- Go through rows 1 to end (exclude 0 since already fully rolled up north)
- Process rocks (O) in that row; check if the previous row (up) is empty:
    - if empty, roll up updating the grid in the current position (.) and next position (O)
    - Continue until row above is not empty or already reached first row

RollSouth 
- Go through 2nd to last row down to row 0 (exclude last since already fully rolled down south)
- Process rocks (O) in that row; check if next row (down) is empty:
    - if empty, roll down updating the grid in current (.) and next position (O)
    - Continue until row below is not empty or already reached last row

RollWest / RollEast 
- Similar to RollNorth and RollSouth, but this time on the x-axis
'''