# Advent of Code 2023 Day 16
# John Roy Daradal 

from aoc import *

reflector = {
    '/' : {
        U : R, 
        D : L, 
        R : U, 
        L : D,
    },
    '\\' : {
        U : L, 
        D : R,
        L : U, 
        R : D,
    },
}

def data(full: bool) -> list[str]:
    return readLines(23, 16, full)

def solve() -> Solution:
    grid = data(full=True)
    
    # Part 1
    count1 = countEnergized(grid, (0,0), R)

    # Part 2 
    yend, xend = getBounds(grid)
    ymax, xmax = yend-1, xend-1
    maxCount = 0
    # Process left and right edges 
    for row in range(0, yend):
        for col, d in [(0, R), (xmax, L)]:
            count = countEnergized(grid, (row,col), d)
            maxCount = max(maxCount, count)
    # Process top and bottom edges 
    for col in range(0, xend):
        for row, d in [(0, D), (ymax, U)]:
            count = countEnergized(grid, (row,col), d)
            maxCount = max(maxCount, count)

    return newSolution(count1, maxCount)

def countEnergized(grid: list[str], start: coords, d: delta) -> int:
    bounds = getBounds(grid)
    q: list[vector] = [(start, d)]
    energized: dict[coords, list[delta]] = defaultdict(list)
    while len(q) > 0:
        curr, d = q.pop(0)
        if not insideBounds(curr, bounds): 
            # Skip out-of-bounds positions
            continue 
        if curr in energized and d in energized[curr]: 
            # Skip coords, delta that was already encountered previously = avoid loops
            continue

        energized[curr].append(d)
        y,x = curr
        tile = grid[y][x]
        if tile == '.':
            # Free space = continue in the same direction
            nxt = move(curr, d)
            q.append((nxt, d))
        elif tile in reflector:
            # Reflector = change direction based on reflector
            d2 = reflector[tile][d]
            nxt = move(curr, d2)
            q.append((nxt, d2))
        elif tile == '|':
            if d == U or d == D: # same direction as splitter
                nxt = move(curr, d)
                q.append((nxt, d)) # continue in same direction
            else: # split into 2
                nxt1 = move(curr, U)
                nxt2 = move(curr, D)
                q.append((nxt1, U))
                q.append((nxt2, D))
        elif tile == '-':
            if d == L or d == R: # same direction as splitter 
                nxt = move(curr, d)
                q.append((nxt, d))
            else: # split into 2 
                nxt1 = move(curr, L)
                nxt2 = move(curr, R)
                q.append((nxt1, L))
                q.append((nxt2, R))

    return len(energized)

if __name__ == '__main__':
    do(solve, 23, 16)

'''
Solve: 
- For Part 1, start from (0,0) going right and count the number of energized cells if light starts from here
- For Part 2, start from all points in the edges, and get the max count of energized cells:
    - For left edge, go right; for right edge, go left 
    - For top edge, go down; for bottom edge, go up
- Use BFS to simulate how the light bounces around the grid; start at the starting coords and direction
- Skip light that goes out of bounds from the grid
- Keep track of the cells that have been energized (passed through for any activity) 
  and from what direction the light was coming from
- We can detect loops if light goes back to an energized cell in the same direction
- Check the tile of the current position in the grid:
    - If free space . = continue moving in the same direction
    - If reflector / or \\, change direction based on current dir and reflector, and move there
    - If vertical splitter |:
        - If current direction is up / down, continue moving in same direction
        - Otherwise, split into 2: one up and one down, and add 2 light positions in the new directions
    - If horizontal splitter -:
        - If current direction is left/right, continue moving in same direction
        - Otherwise, split into 2, one left and one right, and add 2 light positions in the new directions
- Return the number of energized cells in the grid
'''