# Advent of Code 2025 Day 04
# John Roy Daradal 

from aoc import *

PaperGrid = list[list[bool]]

def data(full: bool) -> PaperGrid:
    def fn(line: str) -> list[bool]:
        return [x == '@' for x in line]
    return [fn(line) for line in readLines(25, 4, full)]

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    grid = data(full=True)
    bounds = getBounds(grid)
    rows, cols = bounds 
    count = 0
    for row in range(rows):
        for col in range(cols):
            if not grid[row][col]: continue # skip not paper
            activeNeighbors = [(r,c) for r,c in surround8((row,col)) if insideBounds((r,c),bounds) and grid[r][c]]
            if len(activeNeighbors) < 4:
                count += 1
    return count

def part2() -> int:
    grid = data(full=True)
    bounds = getBounds(grid)
    rows, cols = bounds 
    total = 0
    while True:
        grid2: PaperGrid = []
        count = 0
        for row in range(rows):
            line: list[bool] = []
            for col in range(cols):
                if not grid[row][col]: 
                    line.append(False)
                    continue # skip not paper

                activeNeighbors = [(r,c) for r,c in surround8((row,col)) if insideBounds((r,c),bounds) and grid[r][c]]
                if len(activeNeighbors) < 4:
                    line.append(False)
                    count += 1
                else:
                    line.append(True)
            grid2.append(line)
        total += count
        if count == 0: break
        grid = grid2

    return total

if __name__ == '__main__':
    do(solve, 25, 4)

'''
Part1:
- Go through each cell in the grid
- For each paper cell (True), count how many paper neighbors it has (surround8)
- If count < 4, increment the count
- Return the count of paper cells with < 4 paper neighbors

Part2:
- Find the papers to destroy with the process similar to Part 1 
- Remove the papers and form the next grid
- Count the papers destroyed in this round
- Repeat on the resulting grid until no more papers are destroyed
- Return total count of papers destroyed
'''