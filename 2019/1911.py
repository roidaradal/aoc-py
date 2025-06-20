# Advent of Code 2019 Day 11
# John Roy Daradal 

from aoc import *
from intcode import *

def data(full: bool) -> dict[int,int]:
    line = readFirstLine(19, 11, full)
    numbers = toIntList(line, ',')
    memory = defaultdict(int)
    for i,x in enumerate(numbers):
        memory[i] = x 
    return memory

def solve() -> Solution:
    # Part 1
    numbers = data(full=True)
    numPainted = runProgram(numbers, False)

    # Part 2 
    numbers = data(full=True)
    runProgram(numbers, True)

    return newSolution(numPainted, "")

def runProgram(numbers: dict[int,int], startWhite: bool) -> int:
    i, rbase = 0, 0 
    painted: set[coords] = set()
    curr: coords = (0, 0)
    d: delta = U
    outputs: list[int] = []
    
    grid: dict[coords,bool] = defaultdict(bool)
    grid[curr] = startWhite

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
            numbers[idx] = 1 if grid[curr] else 0
            i += 2
        elif cmd == 4: # Output
            m = modes(head, 1)[0]
            out = param2(numbers[i+1], m, rbase, numbers)
            outputs.append(out)
            if len(outputs) == 2:
                out1, out2 = outputs 
                outputs = [] # reset
                grid[curr] = out1 == 1 
                painted.add(curr)
                if out2 == 0:
                    d = leftOf[d]
                elif out2 == 1:
                    d = rightOf[d]
                curr = move(curr, d)
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

    if startWhite:
        pts = list(grid.keys())
        ys = [p[0] for p in pts]
        xs = [p[1] for p in pts]
        y1,y2 = min(ys), max(ys)
        x1,x2 = min(xs), max(xs)
        for y in range(y1,y2+1):
            line = []
            for x in range(x1,x2+1):
                line.append('#' if grid[(y,x)] else ' ')
            print(''.join(line))
    
    return len(painted)

if __name__ == '__main__':
    do(solve, 19, 11)

'''
Solve:
- For Part 1, don't start on white, run the program and output the number of painted cells 
- For Part 2, start on white, run the program, and display the grid to show the message

RunProgram:
- Similar to 1909 Intcode, but with modified input (3) and output (4)
- For input, supply 1 if the current cell in the grid is white (True), else 0
- For output, process outputs in pairs (wait for 2 outputs):
    - First output decides if the current cell will be painted white (if output is 1)
    - Add current position to set of painted cells
    - Second output decides if we turn left (0) or right (1)
    - Move the current position with the new delta
- Return the number of painted cells
'''