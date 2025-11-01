# Advent of Code 2024 Day 25
# John Roy Daradal 

from aoc import *

int5 = tuple[int,int,int,int,int]

def data(full: bool) -> tuple[list[int5], list[int5]]:
    keys: list[int5] = []
    locks: list[int5] = []
    grid: list[str] = []
    for line in readLines(24, 25, full) + ['']:
        if line == '':
            isKey, columns = parseGrid(grid)
            if isKey: 
                keys.append(columns)
            else:
                locks.append(columns)
            grid = []
        else:
            grid.append(line)
    return keys, locks

def solve() -> Solution:
    keys, locks = data(full=True)
    count = 0
    for key in keys:
        for lock in locks:
            if hasNoOverlap(key, lock):
                count += 1
    return newSolution(count, "")

def parseGrid(grid: list[str]) -> tuple[bool, int5]:
    rows, _ = getBounds(grid)
    count: dict[int, int] = defaultdict(int)
    isKey = grid[0][0] == '.'
    for row in range(1, rows-1):
        for col, tile in enumerate(grid[row]):
            if tile == '#':
                count[col] += 1
    columns: int5 = (count[0], count[1], count[2], count[3], count[4])
    return isKey, columns

def hasNoOverlap(key: int5, lock: int5) -> bool:
    return all(k+l <= 5 for k,l in zip(key,lock))

if __name__ == '__main__':
    do(solve, 24, 25)

'''
Solve:
- Parse the grids from input to get the keys and locks:
    - If first row is empty (.), the grid is a key 
    - If first row is not empty (#), the grid is a lock
    - Count the number of # for each column
    - Exclude the first and last row from counting
- Go through all key-lock pairs and check if they overlap
- A key and lock does not overlap if all their columns have a total sum <= 5
- Output the number of non-overlapping key-lock pairs
- No problem for Part 2
'''