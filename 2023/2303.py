# Advent of Code 2023 Day 03
# John Roy Daradal 

import re
from aoc import *

def data(full: bool) -> list[str]:
    return readLines(23, 3, full)

def solve() -> Solution: 
    return newSolution(part1(), part2())

def part1() -> int:
    grid = data(full=True)
    symbols = findSymbols(grid)
    total = sum(findValidNumbers(grid, symbols))
    return total

def part2() -> int:
    grid = data(full = True)
    gears = findGears(grid)
    total = sum(findGearRatios(grid, gears))
    return total

nonSymbol = '0123456789.'
def findSymbols(grid: list[str]) -> set[coords]:
    symbols = set()
    for row, line in enumerate(grid):
        for col, char in enumerate(line):
            if char not in nonSymbol:
                symbols.add((row,col))
    return symbols

def findValidNumbers(grid: list[str], symbols: set[coords]) -> list[int]:
    bounds = getBounds(grid)
    numbers = []
    for row, line in enumerate(grid):
        for m in re.finditer(r'[0-9]+', line):
            start, end = m.start(), m.end()
            rowRange = (row, start, end)
            if hasAdjacentSymbol(rowRange, symbols, bounds):
                number = int(line[start:end])
                numbers.append(number)
    return numbers

def findGears(grid: list[str]) -> set[coords]:
    gears = set()
    for row, line in enumerate(grid):
        for col, char in enumerate(line): 
            if char == '*':
                gears.add((row,col))
    return gears

def findGearRatios(grid: list[str], gears: set[coords]) -> list[int]:
    bounds = getBounds(grid)
    adjacent = defaultdict(list) 
    for row, line in enumerate(grid):
        for m in re.finditer(r'[0-9]+', line):
            start, end = m.start(), m.end()
            rowRange = (row, start, end)
            number = int(line[start:end])
            for c in getAdjacentSymbols(rowRange, gears, bounds):
                adjacent[c].append(number)
    
    numbers = []
    for c in adjacent:
        if len(adjacent[c]) == 2:
            a,b = adjacent[c]
            numbers.append(a * b)
    return numbers

def hasAdjacentSymbol(rowRange: int3, symbols: set[coords], bounds: dims2) -> bool:
    return len(getAdjacentSymbols(rowRange, symbols, bounds)) > 0

def getAdjacentSymbols(rowRange: int3, symbols: set[coords], bounds: dims2) -> list[coords]:
    adjacent = getAdjacent(rowRange, bounds)
    common = symbols.intersection(set(adjacent))
    return sorted(common)

def getAdjacent(rowRange: int3, bounds: dims2) -> list[coords]:
    y1, x1, x2 = rowRange 
    rows, cols = bounds 
    y0, y2 = y1-1, y1+1 
    x0, x3 = x1-1, x2+1
    adjacent = []

    start = x0 if x0 >= 0 else x1 
    end   = x3 if x3 <= cols else x2 
    addAbove = y0 >= 0 
    addBelow = y2 < rows 
    for x in range(start,end):
        if addAbove: adjacent.append((y0, x))
        if addBelow: adjacent.append((y2, x))
    if start != x1: adjacent.append((y1, x0))
    if x2 < cols: adjacent.append((y1, x2))
    return adjacent

if __name__ == '__main__':
    do(solve, 23, 3)

'''
Part1:
- Find the symbols in the grid (non-digits or .)
- Find numbers in each row
- For each number, check if there is a symbol in its surrounding coords
- Get the total of the valid numbers (adjacent to a symbol)

Part2:
- Find the gears (*) in the grid 
- Find numbers in each row, similar to Part 1
- For each number, get all adjacent gears in its surrounding coords 
- Keep track of each gear's adjacent numbers 
- Keep only the gears with only 2 adjacent numbers 
- Sum up the product of the gears' 2 adjacent numbers
'''