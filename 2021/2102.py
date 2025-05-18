# Advent of Code 2021 Day 02
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[delta]:
    def fn(line: str) -> delta:
        cmd, x = line.split()
        x = int(x)
        if cmd == 'forward':
            return (0, x)
        elif cmd == 'up':
            return (-x, 0)
        elif cmd == 'down':
            return (x,0)
        else:
            return (0,0)
    return [fn(line) for line in readLines(21, 2, full)]

def part1():
    moves = data(full=True)
    curr = (0,0)
    for d in moves:
        curr = move(curr, d)
    y,x = curr 
    print(x*y) 

def part2():
    moves = data(full=True)
    y, x, a = 0, 0, 0 
    for dy, dx in moves:
        if dy == 0:
            x += dx 
            y += a * dx 
        else:
            a += dy
    print(x*y) 

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Data:
- Convert forward: (0, x)
- Convert up     : (-x,0)
- Convert down   : (x,0)

Part1:
- Start at (0,0) and apply delta moves in succession
- Return product of y * x of final coords

Part2:
- Start at (0,0) and process moves 
- If forward: increase x by dx, and increase y by aim*dx 
- If up/down: increase aim by dy
'''