# Advent of Code 2021 Day 11
# John Roy Daradal 

from aoc import *

def data(full: bool) -> IntGrid:
    return [toIntLine(line) for line in readLines(21, 11, full)]

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    grid = data(full=True)
    total = sum(countFlash(grid) for _ in range(100))
    return total 

def part2() -> int:
    grid = data(full=True)
    i = 0 
    while True:
        i += 1
        if countFlash(grid) == 100:
            break
    return i

def countFlash(grid: IntGrid) -> int:
    rows, cols = getBounds(grid)
    flashed: dict[coords,bool] = {(r,c): False for r in range(rows) for c in range(cols)}

    # Increment energy 
    for row,line in enumerate(grid):
        grid[row] = [x+1 for x in line]

    for row,line in enumerate(grid):
        for col,energy in enumerate(line):
            pt = (row,col)
            if energy > 9 and not flashed[pt]:
                flashOctopus(pt, grid, flashed)

    count = 0
    for pt in flashed:
        if not flashed[pt]: continue 
        row,col = pt 
        grid[row][col] = 0
        count += 1
    return count 

def flashOctopus(c: coords, grid: IntGrid, flashed: dict[coords,bool]):
    flashed[c] = True 
    bounds = getBounds(grid)
    near = [n for n in surround8(c) if insideBounds(n, bounds)]
    for nxt in near:
        row, col = nxt
        grid[row][col] += 1 
        if grid[row][col] > 9 and not flashed[nxt]:
            flashOctopus(nxt, grid, flashed)

if __name__ == '__main__':
    do(solve, 21, 11)

'''
Solve:
- For Part 1, count the total number of flashes after 100 steps
- For Part 2, find the first step number where all 100 octopuses flash

CountFlash:
- For this round, initialize all grid cells to flashed = False 
- Increment all octopus energies by 1 
- Process each octopus in order: if energy > 9 and not yet flashed, octopus flashes:
    - Set octopus flashed = True 
    - Check the surround8 neighbors; keep only those that are within grid bounds 
    - Increment each valid neighbor's energy by 1 
    - If neighbor also exceeds 9 and not yet flashed, call flashOctopus on it recursively
- Count the number of octopus who flashed in this round
- The energies of octopus that flashed are reset to 0

'''