# Advent of Code 2024 Day 18
# John Roy Daradal 

from aoc import *

Grid = dict[coords,bool]

def data(full: bool) -> list[coords]:
    def fn(line: str) -> coords:
        x,y = toInt2(line, ',')
        return (y,x)
    return [fn(line) for line in readLines(24, 18, full)]

def solve() -> Solution:
    corrupted = data(full=True)
    bounds = (71,71)

    # Part 1
    count = 1024
    grid: Grid = defaultdict(bool)
    for i in range(count):
        grid[corrupted[i]] = True
    minPath = bfsShortestPath(grid, bounds)

    # Part 2 
    limit = len(corrupted)
    blocker = ''
    for i in range(count, limit):
        grid[corrupted[i]] = True
        sp = bfsShortestPath(grid, bounds)
        if sp == 0:
            y,x = corrupted[i]
            blocker = '%d,%d' % (x,y)
            break

    return newSolution(minPath, blocker)

def bfsShortestPath(grid: Grid, bounds: dims2) -> int:
    rows,cols = bounds
    start: coords = (0,0)
    goal: coords = (rows-1,cols-1)
    visited: set[coords] = set()
    q: list[tuple[coords, int]] = [(start, 0)]
    while len(q) > 0:
        curr, steps = q.pop(0)
        if curr == goal:
            return steps 
        if curr in visited: continue 
        visited.add(curr)
        for nxt in surround4(curr):
            if not insideBounds(nxt, bounds): continue 
            if grid[nxt]: continue # corrupted
            q.append((nxt, steps+1))
    return 0

if __name__ == '__main__':
    do(solve, 24, 18)

'''
Part1:
- Use a defaultdict to represent the grid, so we can lazily build it
- For the first 1024 coordinates, make the grid at that cell corrupted
- Use BFS to find the shortest path from the top-left to bottom-right corner
  within the grid, where you cannot go out of bounds, and you cannot pass through corrupted cells

Part2:
- Starting with the 1025th coordinate, add the corrupted cells to the grid one by one
- Use BFS to check if there is a path from the start (TL) to goal (BR)
- If BFS returned 0 (no path), then we have found the corrupting cell that will make the grid non-passable
'''