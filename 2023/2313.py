# Advent of Code 2023 Day 13
# John Roy Daradal 

from typing import Iterable
from aoc import *

Grid = list[str]

def data(full: bool) -> list[Grid]:
    grids: list[Grid] = []
    grid: Grid = []
    for line in readLines(23, 13, full):
        if line == '':
            grids.append(grid)
            grid = []
        else:
            grid.append(line)
    grids.append(grid)
    return grids 

def solve() -> Solution:
    grids = data(full=True)

    # Part 1 
    fn1 = lambda grid: findMirror(grid, 0)
    total1 = getTotal(grids, fn1)

    # Part 2 
    fn2 = lambda grid: findMirror(grid, 1)
    total2 = getTotal(grids, fn2) 

    return newSolution(total1, total2)

def findMirror(grid: Grid, goalDiff: int) -> int:
    rows, cols = getBounds(grid)

    for col in range(1, cols):
        left = col 
        right = cols-col 
        size = min(left, right)
        diff = 0 
        for i in range(size):
            x1 = col - (i+1)
            x2 = col + i 
            half1 = [grid[y][x1] for y in range(rows)]
            half2 = [grid[y][x2] for y in range(rows)]
            diff += countDiff(half1, half2)
        if diff == goalDiff:
            return col * 1
        
    for row in range(1, rows):
        above = row 
        below = rows-row 
        size = min(above, below)
        diff = 0 
        for i in range(size):
            y1 = row - (i+1)
            y2 = row + i 
            half1 = grid[y1]
            half2 = grid[y2]
            diff += countDiff(half1, half2)
        if diff == goalDiff:
            return row * 100 
        
    return 0

def countDiff(a: Iterable, b: Iterable) -> int:
    return sum(1 for x,y in zip(a,b) if x != y)

if __name__ == '__main__':
    do(solve, 23, 13)

'''
Solve:
- For Part 1, find the reflection line where the halves are perfectly symmetrical (diff=0)
- For Part 2, find the reflection line that allows for a difference of 1 for the halves
- To find the mirror reflection line, go through columns first, then rows
- Go through columns 1 to the end:
    - Left half's size is the column number, right half's size is numCols-column 
    - Choose the smaller size between left and right half
    - Starting from the current column, compare the left and right half columns, 
      size columns to left and size columns to the right
    - If the total difference at this column as reflection line is goal difference, return column
- If not yet found, go through rows 1 to the end:
    - Above half's size = row number, below half's size is numRows-row 
    - Choose the smaller size between above and below half 
    - Starting from the current row, compare the above and below rows,
      size columns above and size columns below 
    - If the total difference at this row as reflection is goal difference, return row * 100
'''