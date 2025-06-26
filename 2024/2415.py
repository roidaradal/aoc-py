# Advent of Code 2024 Day 15
# John Roy Daradal 

from aoc import *

Grid = list[list[str]]

class Problem:
    def __init__(self):
        self.grid: Grid = []
        self.curr: coords = (0,0)
        self.moves: list[delta] = []

def data(expand: bool, full: bool) -> Problem:
    T: dict[str,delta] = {'<': L, '>': R, '^': U, 'v': D}
    E: dict[str,str] = {'#': '##', 'O': '[]', '.': '..', '@': '@.'}
    p = Problem()
    getMoves = False 
    for line in readLines(24, 15, full):
        if line == '':
            getMoves = True 
        elif getMoves:
            p.moves += [T[x] for x in line]
        else:
            if expand: line = ''.join(E[x] for x in line)
            p.grid.append(list(line))
    for y,line in enumerate(p.grid):
        for x,char in enumerate(line):
            if char == '@':
                p.curr = (y,x)    
    return p

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    p = data(expand=False, full=True)
    grid = p.grid 

    curr = p.curr 
    for d in p.moves:
        ny,nx = move(curr, d)
        nxt = grid[ny][nx]

        if nxt == '#':
            pass # hit wall, do nothing
        elif nxt == '.':
            y,x = curr 
            grid[y][x] = '.'    # move robot
            grid[ny][nx] = '@'  # to free space
            curr = (ny,nx)
        else: 
            # find '.' or '#' 
            sy, sx = ny, nx 
            found = False 
            while True:
                sy, sx = move((sy, sx), d)
                if grid[sy][sx] == '#':
                    break # hit a wall, do nothing
                elif grid[sy][sx] == '.':
                    found = True # found free space
                    break 
            if found:
                y,x = curr 
                grid[y][x] = '.'    # move robot from old position
                grid[ny][nx] = '@'  # to new position
                grid[sy][sx] = 'O'  # move last pushed box to found space
                curr = (ny,nx)
    
    return gridScore(grid)

def part2() -> int:
    p = data(expand=True, full=True)
    grid = p.grid

    curr = p.curr 
    for d in p.moves:
        ny,nx = move(curr, d)
        nxt = grid[ny][nx]

        if nxt == '#':
            pass # hit wall, do nothing
        elif nxt == '.':
            y,x = curr 
            grid[y][x] = '.'    # move robot
            grid[ny][nx] = '@'  # to free space
            curr = (ny,nx)
        else: # next is boxes 
            if d == L:
                curr = slideHorizontal(grid, curr, -1)
            elif d == R:
                curr = slideHorizontal(grid, curr, 1)
            elif d == U:
                curr = slideVertical(grid, curr, -1)
            elif d == D:
                curr = slideVertical(grid, curr, 1)

    return gridScore(grid)

def gridScore(grid: Grid) -> int:
    total = 0
    for row, line in enumerate(grid):
        for col, char in enumerate(line):
            if char == 'O' or char == '[':
                total += (row*100) + col 
    return total

def slideHorizontal(grid: Grid, curr: coords, step: int) -> coords:
    y, sx = curr 
    while True:
        sx += step 
        pixel = grid[y][sx]
        if pixel == '#':
            return curr # stuck = dont move 
        elif pixel == '.':
            break       # found free space

    cx = curr[1]
    opp = -step 
    for x in range(sx, cx, opp):
        grid[y][x] = grid[y][x+opp]
    grid[y][cx] = '.'
    nx = cx+step
    return (y, nx)

def slideVertical(grid: Grid, curr: coords, step: int) -> coords:
    y,x = curr 
    slide: set[coords] = set()
    q: list[coords] = [(y+step, x)]
    while len(q) > 0:
        y,x = q.pop(0)

        # Add pair 
        pair: coords = (y,x+1) if grid[y][x] == '[' else (y,x-1)
        if pair not in slide:
            q.append(pair)
        
        # Check next 
        ny = y+step 
        pixel = grid[ny][x]
        if pixel == '#':
            return curr # stuck = dont move
        elif pixel == '.':
            pass 
        else: # pixel is [ or ], found another box 
            q.append((ny, x))

        slide.add((y,x))

    isGoingDown = step == 1
    for y,x in sorted(slide, reverse=isGoingDown):
        grid[y+step][x] = grid[y][x]
        grid[y][x] = '.'

    y,x = curr 
    ny = y+step
    grid[ny][x] = '@'
    grid[y][x] = '.'
    return (ny, x)

if __name__ == '__main__':
    do(solve, 24, 15)

'''
Part1:
- Process the moves in order, start with robot position where @ is in the grid 
- Try to move to the next position:
    - if next position contains a wall #, do nothing (cannot move)
    - if next position is free (.), move the robot here 
    - Otherwise, there is a box (O); continue moving in the current direction 
      and find a wall (stuck, cannot move) or free space 
    - If we find a free space, move the robot to the next position and move a box 
      to the found free space
- Output the grid score: sum of (row*100) + col of box positions

Part2:
- Expand the input grid by translating the pixels with their replacements
- Similar processing to Part 1, except for when we find a box [ or ]
- Depending on the current delta, we slide horizontally (L or R) or vertically (U or D), 
  moving along the boxes that are also pushed up/down or slid left/right
- Slide Horizontal (left / right):
    - Go sideways (left/right) on the same row 
    - If we find a wall #, stop and don't move (curr stays the same)
    - If we find a free space, move all pixels from current to the free space forward/backward
      and the next step is the new current position of the robot 
- Slide Vertical (up / down):
    - Keep track of the pixels that are affected by the slide up/down
    - Start with the pixel above/below the current: this will be slid 
    - Check if its pair is not yet in the slide set; if not, add the pair to the queue 
    - We add the pair since the box [] is two pixels that need to move together 
    - Check the dequeued pixel's next pixel (up/down):
        - If find a wall, stop and dont move (curr stays the same)
        - If we find a free space, we simply add the dequeued pixel to slide set 
        - If we find another box [ or ] above/below, we enqueue that next pixel since it should also be moved 
    - After processing all moving boxes, go through them in order, sorted by y-axis
    - If going down, reverse the order 
    - Slide up/down the pixels in the slide set and update the curr with the next step
'''