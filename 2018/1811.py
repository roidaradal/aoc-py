# Advent of Code 2018 Day 11
# John Roy Daradal 

from aoc import *

def data(full: bool) -> int:
    line = readLines(18, 11, full)[0]
    return int(line)

def solve():
    serial = data(full=True)
    grid = buildGrid(serial) 

    _, row, col = findMaxPower(grid, 3)
    print('%d,%d' % (col,row))

    row, col, side = findMaxPowerSide(grid)
    print('%d,%d,%d' % (col,row,side))

rows, cols = 300, 300
def buildGrid(serial: int) -> IntGrid:
    grid: IntGrid = createGrid(0, rows, cols)
    for row in range(rows):
        for col in range(cols):
            grid[row][col] = computePower(row+1, col+1, serial)
    return grid

def computePower(y: int, x: int, serial: int) -> int:
    rack = x+10 
    power = rack * y 
    power += serial 
    power *= rack 
    digits = str(power)
    digit = 0 if len(digits) < 3 else int(digits[-3])
    return digit - 5

def findMaxPower(grid: IntGrid, side: int) -> int3:
    squares: list[int3] = []
    s = side-1
    for row in range(0, rows-s):
        for col in range(0, cols-s):
            score = sum(sum(grid[y][x] for x in range(col, col+side)) for y in range(row,row+side))
            squares.append((score, row, col))
    score, row, col = max(squares)
    return score, row+1, col+1

def findMaxPowerSide(grid: IntGrid) -> int3:
    squares: list[int4] = []
    power: dict[coords,int] = {}
    for side in range(1, rows+1):
        # print(side)
        s = side-1
        sideSquares: list[int4] = []
        for row in range(0,rows-s):
            for col in range(0,cols-s):
                if side == 1:
                    score = grid[row][col]
                else: 
                    score = power[(row,col)]
                    y = row+s  # add extra row
                    score += sum(grid[y][x] for x in range(col,col+side)) 
                    x = col+s  # add extra col 
                    score += sum(grid[y][x] for y in range(row,row+s)) # don't double count the bottom-right cell
                power[(row,col)] = score 
                sideSquares.append((score, row, col, side))
        best = max(sideSquares)
        squares.append(best)

    _, row, col, side = max(squares)
    return row+1, col+1, side

if __name__ == '__main__':
    do(solve)

'''
Part1:
- Build the 300x300 number grid by using the formula to compute the cell's power
- Go through 3x3 windows in the grid and get their total powers
- Output the top-left corner of the 3x3 window with maximum total power

Part2:
- Similar to Part 1, but not limited to 3x3 windows, now allowed to have squares from 1x1 to 300x300
- In order to avoid repetitive computation, save the previously computed power for the top-left corner of previous side size
- Base case: side = 1, just set power total = grid power value
- For bigger sides, add an extra row and extra column to the power computation
- For each side, only keep the maximum score top-left corner 
- After going through all sides, output the top-left corner and side with max total power
'''