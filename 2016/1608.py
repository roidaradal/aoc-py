# Advent of Code 2016 Day 08
# John Roy Daradal 

from aoc import *

class Problem:
    def __init__(self):
        self.grid = []
        self.commands = []

def data(full: bool) -> Problem:
    problem = Problem()
    rows,cols = 6,50
    problem.grid = [[False for _ in range(cols)] for _ in range(rows)]
    for line in readLines(16, 8, full):
        p = line.split()
        if p[0] == 'rect':
            problem.commands.append(('rect', toDims2(p[1], 'x')))
        elif p[1] == 'column':
            col = int(p[2].split('=')[1])
            rot = int(p[-1])
            problem.commands.append(('col', (col,rot)))
        elif p[1] == 'row':
            row = int(p[2].split('=')[1])
            rot = int(p[-1])
            problem.commands.append(('row', (row,rot)))
    return problem

def solve():
    problem = data(full=True)
    grid = problem.grid 
    for action,c in problem.commands:
        if action == 'rect':
            turnOn(grid, c)
        elif action == 'row':
            rotateRow(grid, c)
        elif action == 'col':
            rotateCol(grid, c)
    count = sum(sum(line) for line in grid)
    print(count) 
    displayGrid(grid)


def turnOn(grid: list[list[bool]], c: dims2):
    cols,rows = c 
    for row in range(rows):
        for col in range(cols):
            grid[row][col] = True

def rotateRow(grid: list[list[bool]], c: int2):
    rowIdx, steps = c 
    row = grid[rowIdx]
    for _ in range(steps):
        row = row[-1:] + row[:-1]
    grid[rowIdx] = row 

def rotateCol(grid: list[list[bool]], c: int2):
    colIdx, steps = c 
    col = [line[colIdx] for line in grid]
    for _ in range(steps):
        col = col[-1:] + col[:-1]
    for row in range(len(grid)):
        grid[row][colIdx] = col[row]

def displayGrid(grid: list[list[bool]]):
    for line in grid:
        out = ''.join('#' if x else ' ' for x in line)
        print(out)

if __name__ == '__main__':
    do(solve)

'''
Solve:
- Start with the grid all turned off (False)
- Process each command, and output the number of turned on cells in the grid after
- For rect command, turn on the top-left square bounded by cols,rows
- For rotate row, extract the grid row by index, and rotate it step no. of times 
- For rotate col, extract the grid col by index, and rotate it step no. of times
- To rotate a row/col, take the last element and put it in first position
- For part 2, display the grid to reveal the message
'''