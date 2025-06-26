# Advent of Code 2021 Day 05
# John Roy Daradal 

from aoc import *

line = tuple[coords, coords]

def data(full: bool) -> tuple[list[line], dims2]:
    rows, cols = 0, 0 
    lines = []
    for text in readLines(21, 5, full):
        head, tail = splitStr(text, '->')
        x1,y1 = toIntList(head, ',')
        x2,y2 = toIntList(tail, ',')
        rows = max(rows, y1, y2)
        cols = max(cols, x1, x2)
        lines.append(((y1,x1),(y2,x2)))
    return (lines, (rows+1, cols+1))

def solve() -> Solution:
    lines, bounds = data(full = True)

    # Part 1
    count1 = countIntersection(lines, bounds, False)

    # Part 2
    count2 = countIntersection(lines, bounds, True)

    return newSolution(count1, count2)

def countIntersection(lines: list[line], bounds: dims2, withDiagonal: bool) -> int:
    rows, cols = bounds 
    g = [[0 for _ in range(cols)] for _ in range(rows)]
    for (y1,x1),(y2,x2) in lines:
        if x1 == x2:
            addVertical(g, y1, y2, x1)
        elif y1 == y2:
            addHorizontal(g, x1, x2, y1)
        elif withDiagonal and abs(y1-y2) == abs(x1-x2):
            addDiagonal(g, x1, y1, x2, y2)
    return sum(sum(1 for x in range(cols) if g[y][x] > 1) for y in range(rows))

def addVertical(g: list[list[int]], y1: int, y2: int, x: int):
    y1, y2 = sorted([y1, y2])
    for y in range(y1, y2+1):
        g[y][x] += 1

def addHorizontal(g: list[list[int]], x1: int, x2: int, y: int): 
    x1, x2 = sorted([x1, x2])
    for x in range(x1, x2+1):
        g[y][x] += 1 

def addDiagonal(g: list[list[int]], x1: int, y1: int, x2: int, y2: int):
    if x1 < x2:
        xs = list(range(x1,x2+1))    # forward 
    else:
        xs = list(range(x1,x2-1,-1)) # backward
    if y1 < y2:
        ys = list(range(y1,y2+1))    # forward 
    else:
        ys = list(range(y1,y2-1,-1))  # backward
    for i in range(len(xs)):
        y, x = ys[i], xs[i]
        g[y][x] += 1

if __name__ == '__main__':
    do(solve, 21, 5)

'''
CountIntersection:
- In Part1, dont include diagonals; do this in Part2
- Process each line (y1,x1),(y2,x2):
    - If same col (x1=x2), add vertical line to grid; just need the y1 and y2 bounds
    - If same row (y1=y2), add horizontal line to grid; just need the x1 and x2 bounds
    - If dy (|y1-y2|) == dy (|x1-x2|), add diagonal line
- When adding line, increase count of coords by 1
- Count intersecting coords: those with count > 1
'''