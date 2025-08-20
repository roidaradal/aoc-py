# Advent of Code 2022 Day 22
# John Roy Daradal 

from aoc import *

NONE, FREE, WALL = ' ', '.', '#'
scoreOf: dict[delta, int] = {R: 0, D: 1, L: 2, U: 3}
TOP, BOT, FRONT, BACK, LEFT, RIGHT = 'top', 'bot', 'front', 'back', 'left', 'right'
cubeFace: dict[coords, str] = {
    (0,1): TOP,
    (0,2): RIGHT, 
    (1,1): FRONT, 
    (2,0): LEFT, 
    (2,1): BOT, 
    (3,0): BACK,
}

def data(full: bool) -> tuple[list[str], list[str|int]]:
    lines = readLines(22, 22, full, strip=False)
    grid = [line.strip('\n') for line in lines[0:-2]]
    maxLen = max(len(line) for line in grid)
    grid = [line.ljust(maxLen) for line in grid]
    steps: list[str|int] = []
    digit: list[str] = []
    for x in lines[-1].strip():
        if x == 'L' or x == 'R':
            steps.append(int(''.join(digit)))
            steps.append(x)
            digit = []
        else:
            digit.append(x)
    steps.append(int(''.join(digit)))
    return grid, steps

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    grid, steps = data(full=True)
    bounds = analyzeGrid(grid)
    curr: coords = (0, bounds['min-col'][0])
    d: delta = R
    for step in steps:
        if type(step) == str:
            if step == 'L':
                d = leftOf[d]
            elif step == 'R':
                d = rightOf[d]
        elif type(step) == int:
            row, col = curr
            for _ in range(step):
                nxt = move(curr, d)
                ny, nx = nxt 
                if d == R and nx > bounds['max-col'][row]:
                    nx = bounds['min-col'][row]
                elif d == L and nx < bounds['min-col'][row]:
                    nx = bounds['max-col'][row]
                elif d == D and ny > bounds['max-row'][col]:
                    ny = bounds['min-row'][col]
                elif d == U and ny < bounds['min-row'][col]:
                    ny = bounds['max-row'][col]
                if grid[ny][nx] == WALL: 
                    break 
                else: 
                    curr = (ny,nx)

    return computePassword(curr, d)

def part2() -> int:
    grid, steps = data(full=True)
    curr: coords = (0,50)
    d: delta = R
    for step in steps:
        if type(step) == str:
            if step == 'L':
                d = leftOf[d]
            elif step == 'R':
                d = rightOf[d]
        elif type(step) == int:
            for _ in range(step):
                nxt, nd = cubeMove(curr, d)
                ny,nx = nxt 
                if grid[ny][nx] == WALL:
                    break 
                else:
                    curr, d = nxt, nd 

    return computePassword(curr, d)

def analyzeGrid(grid: list[str]) -> dict[str, dict[int,int]]:
    bounds: dict[str, dict[int,int]] = {
        'min-row': {},
        'max-row': {},
        'min-col': {},
        'max-col': {},
    }
    rows, cols = getBounds(grid)
    maxRow, maxCol = rows-1, cols-1

    # Process by row
    for row in range(rows):
        for col in range(cols):
            tile = grid[row][col]
            if col == 0 and tile != NONE:
                bounds['min-col'][row] = col 
            elif col > 0 and tile != NONE and grid[row][col-1] == NONE:
                bounds['min-col'][row] = col 

            if col == maxCol and tile != NONE:
                bounds['max-col'][row] = col 
            elif col < maxCol and tile != NONE and grid[row][col+1] == NONE: 
                bounds['max-col'][row] = col
    
    # Process by column 
    for col in range(cols):
        for row in range(rows):
            tile = grid[row][col]
            if row == 0 and tile != NONE: 
                bounds['min-row'][col] = row 
            elif row > 0 and tile != NONE and grid[row-1][col] == NONE:
                bounds['min-row'][col] = row
            
            if row == maxRow and tile != NONE: 
                bounds['max-row'][col] = row 
            elif row < maxRow and tile != NONE and grid[row+1][col] == NONE:
                bounds['max-row'][col] = row
    return bounds

def computePassword(curr: coords, d: delta) -> int:
    y,x = curr 
    y,x = y+1, x+1 # adjust for 1-based index
    password = (1000 * y) + (4 * x) + scoreOf[d]
    return password

def cubeMove(curr: coords, d: delta) -> tuple[coords, delta]:
    y,x = curr 
    ny,nx = move(curr, d)
    nd = d 

    currFace = getFace(curr)
    if currFace == FRONT:
        # U / D = proceed normally
        if d == L and x == 50: # Front to Left
            ny = 100 
            nx = y - 50
            nd = D 
        elif d == R and nx == 100: # Front to Right 
            ny = 49 
            nx = y + 50
            nd = U
    elif currFace == TOP: 
        # D / R = proceed normally
        if d == L and x == 50: # Top to Left
            nx = 0 
            ny = 149 - y
            nd = R
        elif d == U and y == 0: # Top to Back
            nx = 0 
            ny = x + 100
            nd = R
    elif currFace == RIGHT:
        # L = proceed normally 
        if d == R and nx == 150: # Right to Bottom
            nx = 99
            ny = 149 - y
            nd = L
        elif d == D and ny == 50: # Right to Front 
            nx = 99
            ny = x - 50
            nd = L
        elif d == U and y == 0: # Right to Back
            ny = 199 
            nx = x - 100
            nd = U
    elif currFace == BOT:
        # U / L = proceed normally 
        if d == R and nx == 100: # Bottom to Right 
            nx = 149 
            ny = 149 - y
            nd = L
        elif d == D and ny == 150: # Bottom to Back
            nx = 49 
            ny = x + 100
            nd = L
    elif currFace == LEFT:
        # R / D = proceed normally 
        if d == U and y == 100: # Left to Front
            nx = 50 
            ny = x + 50
            nd = R
        elif d == L and x == 0: # Left to Top 
            nx = 50
            ny = 149 - y
            nd = R 
    elif currFace == BACK:
        # U = proceed normally 
        if d == R and nx == 50: # Back to Bottom
            ny = 149 
            nx = y - 100
            nd = U 
        elif d == D and ny == 200: # Back to Right 
            ny = 0 
            nx = x + 100
            nd = D
        elif d == L and x == 0: # Back to Top 
            ny = 0
            nx = y - 100
            nd = D

    return (ny,nx), nd

def getFace(curr: coords) -> str:
    y, x = curr 
    y //= 50 
    x //= 50 
    return cubeFace[(y,x)]

if __name__ == '__main__':
    do(solve, 22, 22)

'''
Part1:
- Analyze the grid to know the ff:
    - min-col and max-col for each row
    - min-row and max-row for each column
    - Bounds are either grid bounds or has free space on the side
- Start at row=0, col=min-col at row 0, and direction = R 
- Process the steps one-by-one:
    - If L or R, turn the direction left or right
    - Otherwise, it's a step count, so we repeat the ff. step times:
        - Check the next position if we move from current position towards current direction
        - Check for wrap-arounds:
            - If going R and new x > max-col of this row, wrap around nx = min-col of row 
            - If going L and new x < min-col of this row, wrap around nx = max-col of row 
            - If going D and new y > max-row of this col, wrap around ny = min-row of col
            - If going U and new y < min-row of this col, 
        - If next position has a wall, we don't move forward and we stop the loop
        - If next position is free, we move forward and make it the current position
- After processing all the steps, we compute the password from our current position and direction:
    (1000*(y+1)) + (4*(x+1)) + scoreOf[d], where scoreOf = {R: 0, D: 1, L: 2, U: 3}

Part2:
- The grid cube is arranged like this:
    .TR     R, L, K are rotated left 1x (their "up" is left side)
    .F.     K = back, B = bottom
    LB.
    K..
- Start at (0,50) with direction = R
- Go through the steps similar to Part 1: if L or R, turn the direction left or right
- We still stop moving forward if we hit a wall for our next position
- Wrapping around when we go out-of-bounds is different, we model going around a cube
- When we enter a new cube face, we have to align the row/col from where they intersect, 
  and adjust the direction based on the orientation of the face
- Get the cube face of the current position (see diagram above):
    - Since the cube faces are 50x50, we can compute the bounds of the 3 columns and 4 rows
    - The column bounds are 0, 50, 100, 150
    - The row bounds are 0, 50, 100, 150, 200
    - We can simplify the cube face by dividing the row and col of the grid position by 50
    - Top:      row = 0..50     col = 50..100   face = (0,1)
    - Right:    row = 0..50     col = 100..150  face = (0,2)
    - Front:    row = 50..100   col = 50..100   face = (1,1)
    - Left:     row = 100..150  col = 0..50     face = (2,0)
    - Bottom:   row = 100..150  col = 50..100   face = (2,1)
    - Back:     row = 150..200  col = 0..50     face = (3,0)
- Face = FRONT:
    - U/D: proceed normally, goes to Top, Back respectively
    - L: wrap around to Left Face   (enter from row 100, col = y-50)    new dir = D 
    - R: wrap around to Right Face  (enter from row 49, col = y+50)     new dir = U
- Face = TOP:
    - D/R: proceed normally, goes to Front, Right respectively
    - L: wrap around to Left Face   (enter from col 0, row = 149-y)     new dir = R
    - U: wrap around to Back Face   (enter from col 0, row = x+100)     new dir = R
- Face = RIGHT:
    - L: proceed normally, goes to Top 
    - R: wrap around to Bottom Face (enter from col 99, row = 149-y)    new dir = L 
    - D: wrap around to Front Face  (enter from col 99, row = x-50)     new dir = L 
    - U: wrap around to Back Face   (enter from row 199, col = x-100)   new dir = U
- Face = BOT:
    - U/L: proceed normally, goes to Front, Left respectively 
    - R: wrap around to Right Face  (enter from col 149, row = 149-y)   new dir = L
    - D: wrap around to Back Face   (enter from col 49, row = x+100)    new dir = L  
- Face = LEFT: 
    - R/D: proceed normally, goes to Bottom, Back respectively
    - U: wrap around to Front Face  (enter from col 50, row = x+50)     new dir = R 
    - L: wrap around to Top Face    (enter from col 50, row = 149-y)    new dir = R
- Face = BACK:
    - U: proceed normally, goes to Left
    - R: wrap around to Bottom Face (enter from row 149, col = y-100)   new dir = U 
    - D: wrap around to Right Face  (enter from row 0, col = x+100)     new dir = D 
    - L: wrap around to Top Face    (enter from row 0, col = y-100)     new dir = D
- After processing all the steps, compute the password from current position and direction, similar to Part 1
'''