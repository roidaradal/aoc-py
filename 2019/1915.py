# Advent of Code 2019 Day 15
# John Roy Daradal 

from aoc import *
from intcode import *

def data(full: bool) -> dict[int,int]:
    line = readFirstLine(19, 15, full)
    numbers = toIntList(line, ',')
    memory = defaultdict(int)
    for i,x in enumerate(numbers):
        memory[i] = x 
    return memory

def solve() -> Solution:
    numbers = data(full=True)
    grid, goal = runProgram(numbers) 

    # Part 1 
    steps1 = bfsExploration(grid, (0,0), goal, display=False)

    # Part 2
    steps2 = bfsExploration(grid, goal, None, display=False)

    return newSolution(steps1, steps2)

def nextMove(curr: coords, grid: dict[coords,int]) -> tuple[int, coords]:
    options: list[tuple[int, int, int, coords]] = []
    for i,d in enumerate([U, D, L, R]):
        moveCode = i+1
        nxt = move(curr, d)
        if nxt not in grid: # favor exploration
            options.append((0, 0, moveCode, nxt))
        elif grid[nxt] >= 0: # non-negative = free space
            options.append((1, grid[nxt], moveCode, nxt))
    _, _, moveCode, nxt = min(options)
    return moveCode, nxt

def runProgram(numbers: dict[int, int]) -> tuple[dict[coords,int], coords]:
    i, rbase = 0, 0 
    curr: coords = (0,0)
    nxt: coords = (0,0)
    grid: dict[coords,int] = {} # -1 for wall, last visited for free
    grid[curr] = 0
    steps = 0
    while True:
        word = str(numbers[i])
        head, tail = word[:-2], word[-2:]
        cmd = int(tail)
        if cmd == 99: break 

        if cmd in (1,2,7,8): # Add, Multiply, LessThan, Equals
            in1, in2, out = numbers[i+1], numbers[i+2], numbers[i+3]
            m1, m2, m3 = modes(head, 3)
            a = param2(in1, m1, rbase, numbers)
            b = param2(in2, m2, rbase, numbers)
            c = index(out, m3, rbase)
            if cmd == 1:
                numbers[c] = a + b
            elif cmd == 2:
                numbers[c] = a * b
            elif cmd == 7: 
                numbers[c] = 1 if a < b else 0
            elif cmd == 8:
                numbers[c] = 1 if a == b else 0
            i += 4
        elif cmd == 3: # Input
            m = modes(head, 1)[0]
            idx = index(numbers[i+1], m, rbase)
            moveCode, nxt = nextMove(curr, grid)
            numbers[idx] = moveCode
            steps += 1
            i += 2
        elif cmd == 4: # Output
            m = modes(head, 1)[0]
            output = param2(numbers[i+1], m, rbase, numbers)
            if output == 0: # wall
                grid[nxt] = -1
                grid[curr] = steps
            elif output == 1: # open space
                curr = nxt 
                grid[curr] = steps
            elif output == 2:  # oxygen system
                curr = nxt 
                grid[curr] = steps
                break
            i += 2 
        elif cmd == 9: # relative base 
            m = modes(head, 1)[0]
            jmp = param2(numbers[i+1], m, rbase, numbers)
            rbase += jmp 
            i += 2
        elif cmd == 5 or cmd == 6: #Jump-if-True/False
            p1, p2 = numbers[i+1], numbers[i+2]
            m1, m2 = modes(head, 2)
            isZero = param2(p1, m1, rbase, numbers) == 0
            doJump = isZero if cmd == 6 else (not isZero)
            if doJump:
                i = param2(p2, m2, rbase, numbers)
            else:
                i += 3
    
    return grid, curr

def displayGrid(grid: dict[coords,int], curr: coords, goal: coords|None, visited: dict[coords,int]):
    ys = [c[0] for c in grid.keys()]
    xs = [c[1] for c in grid.keys()]
    y1, x1 = min(ys), min(xs)
    y2, x2 = max(ys), max(xs)
    os.system('clear')
    for y in range(y1,y2+1):
        row = []
        for x in range(x1,x2+1):
            pt = (y,x)
            pixel = ' '
            if pt == (0,0):
                pixel = 'S'
            elif pt == curr:
                pixel = 'O'
            elif pt == goal:
                pixel = 'X'
            elif pt in visited:
                pixel = '.'
            elif pt not in grid:
                pixel = '?'
            elif pt in grid and grid[pt] < 0:
                pixel = '#'
            row.append(pixel)
        print(''.join(row))

def bfsExploration(grid: dict[coords,int], start: coords, goal: coords|None, display: bool = False) -> int:
    visited = {}
    q = [(start, 0)]
    maxSteps = 0
    while len(q) > 0:
        curr, steps = q.pop(0)
        if curr in visited: continue 
        visited[curr] = steps 
        maxSteps = max(maxSteps, steps)
        if display: displayGrid(grid, curr, goal, visited)
        if goal != None and curr == goal:
            return steps
        for nxt in surround4(curr):
            if nxt in visited: continue 
            if nxt not in grid or grid[nxt] < 0: continue # skip unexplored and wall
            q.append((nxt, steps+1))
    return maxSteps

if __name__ == '__main__':
    do(solve, 19, 15)

'''
Solve: 
- Run the program to explore the grid and find the coords of the oxygen system 
- For Part 1, use BFS to find shortest path from (0,0) to the goal (oxygen), navigating the grid 
- For Part 2, use BFS to explore the grid with no goal (find all reachable), starting from oxygen position:
  this models the spread of the oxygen per minute; return the maximum no. of steps in the exploration
- In BFS exploration, valid next candidates are those not yet visited and is a sure blank space in the grid

RunProgram:
- Similar to 1909 Intcode, but with modified input (3) and output (4)
- Figure out the next move (1, 2, 3, 4) using the current position and what we know from the grid so far:
    - Priority #1: unexplored (not yet in grid)
    - Priority #2: last visited (step number), to avoid thrashing
    - Priority #3: U, D, L, R in this order
    - Pick the next move with min priority and feed it to input
- The output has 3 possibilities:
    - Output = 0, next position is a wall, stay in current position 
    - Output = 1, next position is open, move to it (update current)
    - Output = 2, found the oxygen system
    - Update the last visited (no. of steps) for the current position after each output
- Return the computed grid and coords of oxygen system
'''