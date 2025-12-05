# Advent of Code 2025 Day 04
# John Roy Daradal 

from aoc import *

PaperGrid = list[list[bool]]

def data(full: bool) -> PaperGrid:
    def fn(line: str) -> list[bool]:
        return [x == '@' for x in line]
    return [fn(line) for line in readLines(25, 4, full)]

def solve() -> Solution:
    grid = data(full=True)
    bounds = getBounds(grid)
    total1, total2 = 0, 0
    while True:
        grid2: PaperGrid = []
        count = 0
        for row, line in enumerate(grid):
            line2 = line[:]
            for col, paper in enumerate(line):
                if not paper: continue # skip not paper 
                # check neighbors that are inside bounds and are paper
                paperNeighbors = len([True for r,c in surround8((row,col)) if insideBounds((r,c), bounds) and grid[r][c]])
                if paperNeighbors < 4:
                    line2[col] = False 
                    count += 1
            grid2.append(line2)
        if total1 == 0: total1 = count
        total2 += count
        if count == 0: break
        grid = grid2

    return newSolution(total1, total2)

if __name__ == '__main__':
    do(solve, 25, 4)

'''
Solve:
- Repeatedly update the paper grid by removing the papers with < 4 paper neighbors
- Go through each paper cell in the grid and count their paper neighbors
- Those with < 4 paper neighbors are removed in the resulting grid
- Stop if there are no more papers to remove from the current grid
- For Part 1, output the number of papers removed in the first round
- For Part 2, output the total number of papers removed after all rounds
'''