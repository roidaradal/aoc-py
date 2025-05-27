# Advent of Code 2022 Day 10
# John Roy Daradal 

from aoc import *

CRT = list[list[str]]

def data(full: bool) -> list[strInt]:
    def fn(line: str) -> strInt:
        p = line.split()
        cmd = p[0]
        value = int(p[1]) if cmd == 'addx' else 0
        return cmd, value
    return [fn(line) for line in readLines(22, 10, full)]

def solve():
    commands = data(full=True)
    interest = (20, 60, 100, 140, 180, 220)
    crt = createCRT()
    x, t, total = 1, 0, 0
    for cmd, param in commands:
        steps = 2 if cmd == 'addx' else 1
        for _ in range(steps):
            t += 1
            drawPixel(crt, t, x)
            if t in interest:
                total += t * x 
        x += param 
    print(total)
    displayCRT(crt)

rows, cols = 6, 40 
def createCRT() -> CRT:
    crt: CRT = []
    for _ in range(rows):
        line = ['.'] * cols 
        crt.append(line)
    return crt

def displayCRT(crt: CRT):
    for line in crt:
        print(''.join(line))

def drawPixel(crt: CRT, t: int, x: int):
    row = (t-1) // cols 
    col = (t-1) %  cols 
    pixel = '#' if abs(x-col) <= 1 else '.'
    crt[row][col] = pixel

if __name__ == '__main__':
    do(solve)

'''
Part1:
- Start with x=1, t=0; go through each command
- If addx, takes 2 time cycles; otherwise only 1 
- Increase timestep; if current timestep is of interest, add time * x to total
- Add param to the value of x (if noop, param is 0) 

Part2:
- Initialize CRT to all dots 
- On the same command processing loop as Part 1, draw pixels to the CRT 
- Use the current time to determine the row, col of the CRT to paint 
- Paint '#' if value of |x-col| <= 1
- Display the CRT grid to reveal the letters
'''