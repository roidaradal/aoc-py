# Advent of Code 2016 Day 24
# John Roy Daradal 

from functools import cache
from aoc import *

Grid = tuple[str,...]
digits = '0123456789'
start: coords = (0,0)

def data(full: bool) -> Grid:
    return tuple(readLines(16, 24, full))

def solve() -> Solution:
    grid = data(full=True)
    curr = findStart(grid)

    # Part 1 
    sp1 = findShortestTour(grid, curr, False)

    # Part 2
    sp2 = findShortestTour(grid, curr, True)

    return newSolution(sp1, sp2)

def findStart(grid: Grid) -> coords:
    global start
    for row,line in enumerate(grid):
        for col,tile in enumerate(line):
            if tile == '0':
                start = (row,col)
    return start

def findReachableDigits(grid: Grid, curr: coords) -> list[tuple[coords, int]]:
    reachable: list[tuple[coords, int]] = []
    visited: set[coords] = set()
    q: list[tuple[coords, int]] = [(curr, 0)]
    y,x = curr 
    currDigit = grid[y][x]
    while len(q) > 0:
        curr, steps = q.pop(0)
        if curr in visited: continue 
        visited.add(curr)
        for nxt in surround4(curr):
            ny,nx = nxt 
            nxtTile = grid[ny][nx]
            if nxtTile == '.' and nxtTile not in visited:
                q.append((nxt, steps+1))
            elif nxtTile in digits and nxtTile != currDigit:
                reachable.append((nxt, steps+1))
    return reachable

def nextGrid(grid: Grid, curr: coords, tile: str='.') -> Grid:
    grid2 = [list(line) for line in grid]
    y,x = curr 
    grid2[y][x] = tile
    return tuple(''.join(line) for line in grid2)

@cache 
def findShortestTour(grid: Grid, curr: coords, loopBack: bool) -> int:
    totalSteps = 0
    while True:
        reachable = findReachableDigits(grid, curr)
        if len(reachable) == 0: break # no more reachable

        if len(reachable) > 1:
            minSteps: int = sys.maxsize 
            for nxt, steps in reachable:
                grid2 = nextGrid(grid, curr)
                sp = findShortestTour(grid2, nxt, loopBack)
                sp += steps 
                minSteps = min(minSteps, sp)
            return totalSteps + minSteps
        else:
            nxt, steps = reachable[0]
            grid = nextGrid(grid, curr)
            curr = nxt
            totalSteps += steps
            
    if loopBack:
        grid = nextGrid(grid, start, '0')
        _, steps = findReachableDigits(grid, curr)[0]
        totalSteps += steps

    return totalSteps

if __name__ == '__main__':
    do(solve, 16, 24)

'''
Solve:
- Start at the position of 0 in the grid
- Use functools.cache for findShortestTour as the (grid,curr) state can be repeated in other subproblems
- Find the reachable digits from the current position:
    - Use BFS to explore and find reachable digits 
    - Continue exploring along free spaces (.)
    - If we encounter a digit that is not the current digit, add it to reachable list
    - Take note of how many steps it takes to reach each reachable digit
- If there are no more reachable digits, we break out of the loop (all digits have been visited)
- If there is only one reachable digit, go there:
    - Make the digit's position become the current position
    - Add the steps it takes to get to that digit to the total steps
    - Update the grid by removing the digit, making it free space (.)
- If there are multiple reachable digits, evaluate each one and take the min:
    - For each reachable digit and number of steps it takes to get there, create the next grid 
      where the digit is now removed and replaced with free space
    - Run findShortestPath recursively on this next grid, starting at the reachable digit's position 
    - Take the total steps from the findShortestPath result and the initial steps to reach the digit
    - Find the minimum steps out of the choices, and return it together with the totalSteps (from previous rounds)
- After exiting the loop, if loopBack is enabled (for Part 2):
    - Update the grid by adding back the 0 digit to its original position 
    - Run findReachableDigits (BFS) to get the number of steps it takes to reach from current position to the starting position
    - Add it to the total number of steps
- For Part 1, find the shortest tour that visits all digits starting from 0
- For Part 2, find the shortest tour that visits all digits starting from 0, 
  and end back in the starting position of 0
'''