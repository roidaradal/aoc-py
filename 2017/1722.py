# Advent of Code 2017 Day 22
# John Roy Daradal 

from aoc import *

CLEAN, WEAK, INFECTED, FLAGGED = 0, 1, 2, 3

def data(full: bool) -> list[str]:
    return readLines(17, 22, full)

def solve() -> Solution:
    grid = data(full=True)

    # Part 1 
    count1 = countInfected(grid, 2, 10_000)

    # Part 2 
    count2 = countInfected(grid, 1, 10_000_000)

    return newSolution(count1, count2)

def countInfected(grid: list[str], step: int, rounds: int) -> int:
    # Create grid state
    state: dict[coords, int] = defaultdict(int)
    for row,line in enumerate(grid):
        for col,tile in enumerate(line):
            if tile == '.': continue 
            state[(row,col)] = INFECTED

    # Starting point
    rows, cols = getBounds(grid)
    curr: coords = (rows//2, cols//2)
    d: delta = U

    count = 0 
    for _ in range(rounds):
        # Change direction
        if state[curr] == INFECTED:
            d = rightOf[d]
        elif state[curr] == CLEAN:
            d = leftOf[d]
        elif state[curr] == FLAGGED:
            d = leftOf[leftOf[d]] # reverse
        # Update state based on step
        state[curr] = (state[curr] + step) % 4
        if state[curr] == INFECTED: count += 1 
        # Move forward 
        curr = move(curr, d)
    
    return count

if __name__ == '__main__':
    do(solve, 17, 22)

'''
Solve: 
- Represent the cell states as CLEAN=0, WEAK=1, INFECTED=1, FLAGGED=3
    - For Part 1, we transition from clean <=> infected, so we use (curr+2)%4
    - For Part 2, we transition from clean => weak => infected => flagged => clean, so we use (curr+1)%4
- Start at the middle of the grid, with direction going up 
- Repeat the ff. for the specified number of rounds:
    - If current cell is infected, turn right
    - If current cell is clean, turn left 
    - If current cell is flagged, reverse direction (use two turn lefts)
    - Update the state of the current cell based on the state transition above 
    - Move forward using the current direction
- Count the total number of times a cell got infected during the specified number of rounds
- For Part 1, do 10,000 rounds
- For Part 2, do 10,000,000 rounds
'''