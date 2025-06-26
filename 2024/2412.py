# Advent of Code 2024 Day 12
# John Roy Daradal 

from aoc import *

Grid = list[str]

def data(full: bool) -> Grid:
    return readLines(24, 12, full)

def solve() -> Solution:
    grid = data(full=True)

    # Part 1
    price1 = computeFence(grid, False)

    # Part 2
    price2 = computeFence(grid, True)

    return newSolution(price1, price2)

def computeFence(grid: Grid, mergeSides: bool) -> int:
    Plot.grid = grid
    plots: list[Plot] = []
    done: set[coords] = set()
    rows, cols = getBounds(grid)
    for row in range(rows):
        for col in range(cols):
            pt = (row,col)
            if pt in done: continue 
            points = floodFill(grid, pt)
            done = done.union(points)
            plots.append(Plot(grid[row][col], points, mergeSides))

    price = sum(p.area * p.perimeter for p in plots)
    return price 

def floodFill(grid: Grid, start: coords) -> set[coords]:
    bounds = getBounds(grid)
    y,x = start 
    target = grid[y][x]
    visited: set[coords] = set()
    q: list[coords] = [start]
    while len(q) > 0:
        curr = q.pop(0)
        if curr in visited: continue 
        visited.add(curr)
        for nxt in surround4(curr):
            ny, nx = nxt 
            if nxt in visited or not insideBounds(nxt, bounds): continue 
            if grid[ny][nx] == target:
                q.append(nxt)
    return visited

class Plot:
    grid: Grid = []

    def __init__(self, name: str, points: set[coords], mergeSides: bool):
        self.name = name
        self.points: list[coords] = sorted(points)
        self.area = len(points)
        self.perimeter = self.computePerimeter(mergeSides)
    
    def computePerimeter(self, mergeSides: bool) -> int:
        grid = self.grid 
        bounds = getBounds(grid)
        sides = {'U': U, 'D': D, 'L': L, 'R': R}
        fence: dict[str, list[coords]] = {
            'U': [],
            'D': [],
            'L': [],
            'R': []
        }
        for pt in self.points:
            for k,d in sides.items():
                nxt = move(pt, d)
                y,x = nxt 
                if not insideBounds(nxt, bounds) or grid[y][x] != self.name:
                    fence[k].append(pt)

        if mergeSides:
            fence['U'] = mergeVertical(fence['U'])
            fence['D'] = mergeVertical(fence['D'])
            fence['L'] = mergeHorizontal(fence['L'])
            fence['R'] = mergeHorizontal(fence['R'])

        total = sum(len(f) for f in fence.values())
        return total
 
def mergeVertical(fence: list[coords]) -> list[coords]:
    if len(fence) < 2: return fence 
    fence.sort() # sort by y, tie-breaker: x
    merged: list[coords] = []
    py, px = fence[0]
    for cy, cx in fence[1:]:
        if cy != py or cx-px > 1: # not on same row or not contiguous
            merged.append((py, px))
        py, px = cy, cx 
    merged.append((py, px))
    return merged

def mergeHorizontal(fence: list[coords]) -> list[coords]:
    if len(fence) < 2: return fence
    fence.sort(key=lambda c: (c[1], c[0])) # sort by x, tie-breaker: y
    merged: list[coords] = []
    py, px = fence[0]
    for cy, cx in fence[1:]:
        if cx != px or cy-py > 1: # not on same column or not contiguous 
            merged.append((py, px))
        py, px = cy, cx
    merged.append((py, px))
    return merged

if __name__ == '__main__':
    do(solve, 24, 12)

'''
Solve:
- For Part 1, compute the fence price, where the perimeter is total fenceable plant sides 
- For Part 2, compute the fence price, using the number of sides (merged)
- Group the plants together by performing flood-fill on grid points:
    - If a point has been processed by a previous floodfill, skip it 
    - Use BFS to explore grid cells connected to the starting point
    - Check current cell's 4 neighbors(UDLR) that is inside grid bounds and same plant type
- After one run of flood-fill, a plant group is produced; create a Plot object:
    - Area is the number of points 
    - Compute the perimeter (merged or not)
- Return the total price = area * perimeter of the plots

ComputePerimeter:
- For each plot point, check the 4 sides (UDLR)
- If next point is out-of-bounds or has different plant type, add a fence on this side
- If we need to merge sides, merge the sides horizontally (L,R) or vertically (U,D) to count the number of sides:
    - If there are fewer than 2 points, return as-is 
    - Sort the fence points by (y,x) if vertical, or (x,y) if horizontal
    - Check the contiguous pairs of points: prev, curr 
    - If the 2 points are not on the same row/column, line is broken and we add this point to merged 
    - If on same row/column but not contiguous, (diff of other axis is > 1), line is also broken: add to merged
- The total perimeter is the total number of coordinates with fence for all 4 sides
'''