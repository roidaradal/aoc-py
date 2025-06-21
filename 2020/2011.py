# Advent of Code 2020 Day 11
# John Roy Daradal 

from aoc import *

Grid = list[str]

def data(full: bool) -> Grid:
    return readLines(20, 11, full)

def solve() -> Solution:
    # Part 1 and 2
    counts = []
    for adjacentOnly in [True, False]:
        grid = data(full=True)
        prevState = gridState(grid)

        while True:
            grid = nextGrid(grid, adjacentOnly)
            state = gridState(grid)
            if state == prevState: break 
            prevState = state 

        counts.append(countOccupied(grid))

    count1, count2 = counts
    return newSolution(count1, count2)

def countOccupied(grid: Grid) -> int:
    return sum(sum(1 for char in line if char == '#') for line in grid)

def gridState(grid: Grid) -> str:
    return ''.join(grid)

def nextGrid(grid: Grid, adjacentOnly: bool) -> Grid:
    grid2: Grid = []
    minCount = 4 if adjacentOnly else 5
    for row,line in enumerate(grid):
        line2 = []
        for col,char in enumerate(line):
            if char == '.': # floor doesnt change 
                line2.append('.')
                continue 
            if adjacentOnly:
                taken = countAdjacentTaken(grid, (row,col))
            else:
                taken = countVisibleTaken(grid, (row,col))
            if char == 'L' and taken == 0:
                line2.append('#')
            elif char == '#' and taken >= minCount:
                line2.append('L')
            else:
                line2.append(char)
        grid2.append(''.join(line2))
    return grid2

def countAdjacentTaken(grid: Grid, c: coords) -> int:
    near = surround8(c)
    bounds = getBounds(grid)
    near = [n for n in near if insideBounds(n, bounds)]
    taken = 0
    for y,x in near:
        if grid[y][x] == '#': taken += 1
    return taken

def countVisibleTaken(grid: Grid, c: coords) -> int:
    bounds = getBounds(grid)
    deltas = [U, D, L, R, NE, NW, SE, SW]
    taken = 0
    for d in deltas: 
        y,x = c 
        while True:
            y,x = move((y,x), d)
            if not insideBounds((y,x), bounds): break 
            if grid[y][x] == '.': continue 
            if grid[y][x] == '#': taken += 1 
            break
    return taken

if __name__ == '__main__':
    do(solve, 20, 11)

'''
Solve: 
- Keep track of the previous grid state, to check if it hasn't changed (stop condition)
- Go to the next grid state by changing according to the seat changing rules:
    - Floor (.) doesnt change 
    - Count the number of taken seats adjacent/visible from current seat 
    - If seat is empty L and takenCount == 0, change seat to occupied #
    - If seat is occupied # and takenCount >= (4 or 5, depends on Part 1 / 2), change seat to empty L 
    - Otherwise, seat stays the same
- Stop the loop if the grid state is the same as previous 
- Return the number of occupied (#) seats in the grid after stopping
- Part 1 and 2 differs from the count taken function used

Part 1: CountAdjacentTaken
- Using the surround8 coords (UDLR + diagonals), filter the out-of-bounds coords 
- Count if the adjacent coord has a taken seat #

Part 2: CountVisibleTaken 
- For each of the 8 directions (UDLR + diagonals), try to extend (visible) until stopped
- Starting at current position, extend using the current delta
- Stop if out of bounds; continue extending if floor 
- If we see a taken seat # or empty seat L, we stop extending; increase taken count if #
'''