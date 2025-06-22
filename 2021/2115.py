# Advent of Code 2021 Day 15
# John Roy Daradal 

import heapq
from aoc import *

def data(full: bool) -> IntGrid:
    return [toIntLine(line) for line in readLines(21, 15, full)]

def solve() -> Solution:
    grid = data(full=True)

    # Part 1 
    sp = dijkstras(grid)
    goal = getGoal(grid)
    total1 = sp[goal]

    # Part 2 
    grid = expandGrid(grid)
    sp = dijkstras(grid)
    goal = getGoal(grid)
    total2 = sp[goal]

    return newSolution(total1, total2)

def getGoal(grid: IntGrid) -> coords:
    rows, cols = getBounds(grid)
    return (rows-1, cols-1)

def dijkstras(grid: IntGrid) -> dict[coords, int]:
    start: coords = (0,0)
    bounds = getBounds(grid)
    rows, cols = bounds
    sp: dict[coords,int] = {(r,c): sys.maxsize for r in range(rows) for c in range(cols)}
    sp[start] = 0 
    pq: list[tuple[int,coords]] = []
    heapq.heappush(pq, (0, start))
    while len(pq) > 0:
        _, curr = heapq.heappop(pq)
        for nxt in surround4(curr):
            if not insideBounds(nxt, bounds): continue 
            r,c = nxt 
            if sp[nxt] > sp[curr] + grid[r][c]:
                sp[nxt] = sp[curr] + grid[r][c] 
                heapq.heappush(pq, (sp[nxt], nxt))
    return sp

def expandGrid(grid: IntGrid) -> IntGrid:
    gridRow: IntGrid = []
    for line in grid:
        fullRow: list[int] = []
        fullRow += line 
        prev = line 
        for _ in range(4):
            curr =  [increment(x) for x in prev]
            fullRow += curr 
            prev = curr 
        gridRow.append(fullRow)

    fullGrid: IntGrid = []
    fullGrid += gridRow 
    prevGrid = gridRow 
    for _ in range(4):
        currGrid: IntGrid = []
        for line in prevGrid:
            currGrid.append([increment(x) for x in line])
        fullGrid += currGrid 
        prevGrid = currGrid
    
    return fullGrid

def increment(x: int) -> int:
    x += 1 
    return x if x <= 9 else 1

if __name__ == '__main__':
    do(solve, 21, 15)

'''
Solve: 
- For Part 1, run Dijkstra's algorithm on the grid to the find the shortest path 
  from (0,0) to bottom-right
- For Part 2, expand the grid first, then run Dijkstra's to find the shortest path 
  from (0,0) to bottom-right of expanded grid
- Horizontal grid expansion 4 times: increment the previous fullRow 
- Vertical grid expansion 4 times: Increment the full grid above
- During incrementing, if number goes above 9, it resets back to 1

Dijsktra's Algorithm:
- Use heapq (heap priority queue) for faster computation
- Initialize the shortest path of each cell to maxsize (or inf)
- Start with (0,0) on the priority queue 
- Pop out the pq's min priority item -> current coords
- Check the 4 surrounding neighbors (UDLR) that are within grid bounds 
- If we can improve the shortest path to the neighbor by going from current and adding its value:
  update the shortest path value and add it to the heap pq
'''