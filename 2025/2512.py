# Advent of Code 2025 Day 12
# John Roy Daradal 

from aoc import *

Grid = list[str]

class Puzzle:
    def __init__(self, line: str):
        head, tail = line.split(':')
        w, h = [int(x) for x in head.split('x')]
        self.w = w
        self.h = h
        self.counts = [int(x) for x in tail.split()]
    
def data(full: bool) -> tuple[list[Grid], list[Puzzle]]:
    grids: list[Grid] = []
    puzzles: list[Puzzle] = []
    grid: Grid = []
    for line in readLines(25, 12, full):
        if line.endswith(':'):
            continue 
        elif 'x' in line:
            puzzles.append(Puzzle(line))
        elif line == '':
            grids.append(grid)
            grid = []
        else:
            grid.append(line)
    return grids, puzzles

def solve() -> Solution:
    grids, puzzles = data(full=True)

    areas: dict[int, int] = {}
    for i, grid in enumerate(grids):
        areas[i] = '/'.join(grid).count('#')

    count = 0
    for puzzle in puzzles:
        floorArea = puzzle.w * puzzle.h 
        combArea = sum(areas[i] * count for i,count in enumerate(puzzle.counts))
        if combArea <= floorArea:
            count += 1

    return newSolution(count, "")


if __name__ == '__main__':
    do(solve, 25, 12)

'''
Solve:
- For each grid, compute the area by counting the # 
- For each puzzle, multiply the count of each grid by its area and check that the 
  total does not exceed the given dimensions (w x h)
- Output the number of puzzles where the grids fit inside the given area
- No problem for Part 2
'''