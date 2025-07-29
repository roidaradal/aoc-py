# Advent of Code 2015 Day 25
# John Roy Daradal 

from aoc import *

def data(full: bool) -> coords:
    line = readFirstLine(15, 25, full)
    for rep in ',.': line = line.replace(rep, '')
    parts = splitStr(line, None)
    row, col = int(parts[-3]), int(parts[-1])
    return (row,col)

def solve() -> Solution:
    goal = data(full=True)
    
    prev = 20151125
    curr = 0
    row, col = 2, 1
    while True:
        curr = (prev * 252533) % 33554393
        if (row,col) == goal:
            break 

        if row == 1:
            row, col = col+1, 1
        else:
            row, col = row-1, col+1

        prev = curr

    return newSolution(curr, "")

if __name__ == '__main__':
    do(solve, 15, 25)

'''
Solve:
- Start with 20151125 at (1,1), set this as the initial previous value
- Compute the current value = (prev * 252533) % 33554393
- The position in the grid starts at row=2, col=1
- After each computed code, if row is not yet 1, we move to the top-right diagonal 
  by updating row = row-1, col = col+1
- If the row is already at 1 (first row), we reset the row = col+1, col = 1, 
  since the diagonal ends at row=1, col=X, where X is the row we started at
- Stop if we are currently at the goal cell
- No problem for Part 2
'''