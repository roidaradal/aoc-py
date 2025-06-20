# Advent of Code 2017 Day 14
# John Roy Daradal 

from aoc import *
from knotHash import *
from functools import reduce
from operator import xor

def data(full: bool) -> str:
    return readFirstLine(17, 14, full)

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    key = data(full=True)
    totalBits = lambda i: sum(getBits(key, i))
    indexes = list(range(128))
    return getTotal(indexes, totalBits)

def part2() -> int:
    key = data(full=True)
    grid: list[list[int]] = []
    for i in range(128):
        line = getBits(key, i)
        grid.append(line)

    group: dict[coords,int] = {}
    groupID = 0 
    for row, line in enumerate(grid):
        for col, bit in enumerate(line):
            if (row,col) in group or bit == 0: continue 
            points = floodFill(grid, (row,col))
            for pt in points:
                group[pt] = groupID 
            groupID += 1
    return groupID

def getBits(key: str, x: int) -> list[int]:
    fkey = '%s-%d' % (key, x)
    lengths = [ord(x) for x in fkey]
    numbers = knotHash(lengths, 64)
    result = []
    for i in range(0, knotHashLimit, 16):
        r = reduce(xor, numbers[i:i+16])
        result.append(hexCode(r))
    
    hexString = ''.join(result)
    row = []
    for hexChar in hexString:
        row += toIntLine(toBinary(hexChar))
    return row

def toBinary(hexChar: str) -> str:
    x = int(hexChar, 16)
    return binaryFilled(x, 4)

def floodFill(grid: list[list[int]], start: coords) -> set[coords]:
    bounds = getBounds(grid)
    points: set[coords] = set()
    q: list[coords] = [start]
    while len(q) > 0:
        c = q.pop(0)
        if c in points: continue 
        points.add(c)
        for nxt in surround4(c):
            row, col = nxt 
            if not insideBounds(nxt, bounds): continue 
            if grid[row][col] != 1: continue 
            q.append(nxt)
    return points

if __name__ == '__main__':
    do(solve, 17, 14)

'''
Part1:
- Create the binary representation of the grid to find the free (0) and used (1) spaces 
- Create the binary row for key-x for x from 0 to 127 using getBits
- Output the total number of 1s (used) in the grid 

Part2:
- Build the grid similar to Part 1 
- Go through each grid cell and find its connected component by using BFS flood fill 
- During exploration, check the 4 neighbors (N,E,W,S) and only consider those that are used (1)
- If a cell is already part of a group, skip it
- Output the number of groups in the grid

GetBits:
- Get the ASCII codes for <key>-x, and use those codes as the lengths for knotHash, with 64 rounds 
- This produces 256 numbers: take 16 at a time and xor the numbers to produce a number;
- Combine the 2-digit hexCode representations of the 16 results = 32 hex chars 
- For each hex char, convert it to a 4-digit binary number; combine all = 128 bits
- Return this row of 128 bits
'''