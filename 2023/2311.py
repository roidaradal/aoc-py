# Advent of Code 2023 Day 11
# John Roy Daradal 

import itertools
from aoc import *

def data(full: bool) -> tuple[list[str], list[coords]]:
    grid = readLines(23, 11, full)
    galaxies: list[coords] = []
    for row,line in enumerate(grid):
        for col,char in enumerate(line):
            if char == '#':
                galaxies.append((row,col))
    return grid, galaxies

def solve() -> Solution:
    grid, galaxies = data(full=True)

    # Part 1 
    total1 = computeTotal(grid, galaxies, 2)

    # Part 2 
    total2 = computeTotal(grid, galaxies, 1_000_000)

    return newSolution(total1, total2)

def computeTotal(grid: list[str], galaxies: list[coords], factor: int) -> int:
    rowWeight, colWeight = gridWeights(grid, factor) 
    total = 0
    for c1, c2 in itertools.combinations(galaxies, 2):
        (y1,x1), (y2,x2) = c1, c2 
        y1, y2 = sorted([y1,y2])
        x1, x2 = sorted([x1,x2])
        dy = sum(rowWeight[y] for y in range(y1, y2))
        dx = sum(colWeight[x] for x in range(x1, x2))
        total += dy + dx
    return total

def gridWeights(grid: list[str], factor: int) -> tuple[dict[int,int], dict[int,int]]:
    rowWeight: dict[int,int] = {}
    colWeight: dict[int,int] = {}
    rows, cols = getBounds(grid)
    for row in range(rows):
        isEmpty = all(x == '.' for x in grid[row])
        rowWeight[row] = factor if isEmpty else 1 
    for col in range(cols):
        isEmpty = all(grid[row][col] == '.' for row in range(rows))
        colWeight[col] = factor if isEmpty else 1
    return rowWeight, colWeight 


if __name__ == '__main__':
    do(solve, 23, 11)

'''
Solve:
- For Part 1, weight of empty rows and columns = 2 
- For Part 2, weight of empty rows and columns = 1,000,000
- Get the row and column weights: if non-empty, weight = 1, otherwise use the factor 
- Check each galaxy pair combination and get their weighted Manhattan distance:
    - Total along y = sum of row weights from y1 to y2 
    - Total along x = sum of column weights from x1 to x2
'''