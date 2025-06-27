# Advent of Code 2016 Day 18
# John Roy Daradal 

from aoc import *

def data(full: bool) -> str:
    return readFirstLine(16, 18, full)

def solve() -> Solution:
    line = data(full=True)

    # Part 1 
    safe1 = countSafe(line, 40)

    # Part 2
    safe2 = countSafe(line, 400000)

    return newSolution(safe1, safe2)

def countSafe(line: str, rows: int) -> int:
    cols = len(line)
    curr: list[bool] = [char == '^' for char in line]
    count: int = cols - sum(curr)
    for _ in range(rows-1):
        curr = nextRow(curr)
        count += cols - sum(curr)
    return count

def nextRow(prev: list[bool]) -> list[bool]:
    row: list[bool] = []
    last = len(prev)-1
    for x,center in enumerate(prev):
        left  = False if x == 0    else prev[x-1]
        right = False if x == last else prev[x+1]
        ok1 = left and center and (not right)
        ok2 = (not left) and center and right
        ok3 = left and (not center) and (not right)
        ok4 = (not left) and (not center) and right 
        trap = ok1 or ok2 or ok3 or ok4 
        row.append(trap)
    return row

if __name__ == '__main__':
    do(solve, 16, 18)

'''
Solve:
- For Part 1, produce 40 rows, then count the safe tiles 
- For Part 2, produce 400k rows, then count the safe tiles
- We only keep track of the previous row, as the other rows above don't have effect on the computation 
- Convert the initial line into booleans: True if trap (^) 
- Number of safe tiles in this line is number of tiles - number of True (trap)
- Update the safe tile count at each iteration; repeat rows-1 times:
    - Produce the next row and update the total count 
    - Go through each tile in the previous row as the center 
    - Take the left and right tiles as well, except for first tile and last tile (default to safe: False)
    - Compute if the current tile on this row will be a trap based on the 4 conditions
'''