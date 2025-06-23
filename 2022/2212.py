# Advent of Code 2022 Day 12
# John Roy Daradal 

import heapq
from aoc import *

def data(full: bool) -> tuple[coords, coords, IntGrid]:
    lines = readLines(22, 12, full)
    grid: IntGrid = []
    start: coords = (0,0)
    end: coords = (0,0)
    for r,line in enumerate(lines):
        row = []
        for c,char in enumerate(line):
            x = 0
            if char == 'S':
                start = (r,c)
                x = 1 
            elif char == 'E':
                end = (r,c)
                x = 26 
            else:
                x = ord(char) - 96 
            row.append(x)
        grid.append(row)
    return start, end, grid

def solve() -> Solution:
    start, end, grid = data(full=True)

    # Part 1 
    steps = shortestPath(grid, start, end)

    # Part 2 
    starts: list[coords] = []
    for row,line in enumerate(grid):
        for col,height in enumerate(line):
            if height == 1:
                starts.append((row,col))
    minSteps = sys.maxsize
    for start in starts:
        minSteps = min(minSteps, shortestPath(grid, start, end))

    return newSolution(steps, minSteps)

def shortestPath(grid: IntGrid, start: coords, end: coords) -> int:
    bounds = getBounds(grid)
    rows, cols = bounds
    sp: dict[coords,int] = {(r,c): sys.maxsize for r in range(rows) for c in range(cols)}
    sp[start] = 0 
    pq: list[tuple[int,coords]] = []
    heapq.heappush(pq, (0, start))
    while len(pq) > 0:
        _, curr = heapq.heappop(pq)
        r,c = curr
        currHeight = grid[r][c]
        for nxt in surround4(curr):
            if not insideBounds(nxt, bounds): continue 
            r,c = nxt 
            nxtHeight = grid[r][c]
            if nxtHeight-currHeight > 1: continue 
            if sp[nxt] > sp[curr] + 1:
                sp[nxt] = sp[curr] + 1
                heapq.heappush(pq, (sp[nxt], nxt))
    return sp[end]

if __name__ == '__main__':
    do(solve, 22, 12)

'''
Solve:
- Convert the input grid into an IntGrid, where letters (a-z) are transformed into heights (1-26)
- The S and E cells of the grid indicate the starting and ending cells
- For Part 1, find the shortest path from the starting point to the ending point 
- For Part 2, find all the possible starting points (height = 1), and run shortestPath with each starting point,
  return the minimum number of steps among these runs
- To find the shortest path from start to end, use Dijkstra's algorithm with heapq (for performance)
- For next neighbors, consider the surround4 neighbors that are within grid bounds
- Neighbor is valid if its height is same as current or only differs by 1
- The path cost adjustment is 1 (uniform weight, couting number of steps only)
'''