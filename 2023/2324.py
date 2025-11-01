# Advent of Code 2023 Day 24
# John Roy Daradal 

import itertools
from aoc import *

Stone = tuple[int3, int3]   # (position, velocity)
Line = tuple[float, float]  # m,b in y=mx+b 
Point = tuple[float, float]
int6 = tuple[int,int,int,int,int,int]

def data(full: bool) -> list[Stone]:
    def fn(line: str) -> Stone:
        head, tail = splitStr(line, '@')
        position: int3 = toInt3(head, ',')
        velocity: int3 = toInt3(tail, ',')
        return position, velocity
    return [fn(line) for line in readLines(23, 24, full)]

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    stones = data(full=True)
    start = 200000000000000
    end   = 400000000000000

    # Compute line equations for each stone 
    eqs = [lineEq(stone) for stone in stones]

    count = 0
    for idx1, idx2 in itertools.combinations(range(len(stones)), 2):
        eq1, eq2 = eqs[idx1], eqs[idx2]
        pt = intersectionPoint(eq1, eq2)
        if pt is None: continue 

        insideArea = all(start <= v <= end for v in pt)
        future1 = isFuturePoint(pt, stones[idx1])
        future2 = isFuturePoint(pt, stones[idx2])
        if insideArea and future1 and future2:
            count += 1 
    
    return count

def part2() -> int:
    rawStones = data(full=True)
    stones: list[int6] = []
    for position, velocity in rawStones:
        x,y,z = position 
        dx,dy,dz = velocity 
        stones.append((x,y,z,dx,dy,dz))

    def extract(a: int, b: int, c:int, d: int) -> tuple[list[list[int]], list[int]]:
        A: list[list[int]] = [[r[c], -r[d], r[a], r[b]] for r in stones]
        B: list[int] = [r[b] * r[c] - r[a] * r[d] for r in stones]
        return A, B
    
    def solveEq(A: list[list[int]], B: list[int]) -> list[float]:
        n : list[list[int]] = [a+[b] for a,b in zip(A,B)]
        m = [[float(a)-float(b) for a,b in zip(a, n[4])] for a in n[:4]]

        for i in range(len(m)):
            m[i] = [m[i][k] / m[i][i] for k in range(len(m[i]))]

            for j in range(i+1, len(m)):
                m[j] = [m[j][k] - m[i][k] * m[j][i] for k in range(len(m[i]))]
        
        for i in reversed(range(len(m))):
            for j in range(i):
                m[j] = [m[j][k] - m[i][k] * m[j][i] for k in range(len(m[i]))]
        
        return [r[-1] for r in m]

    x, y, *_ = solveEq(*extract(0,1,3,4))
    z,    *_ = solveEq(*extract(1,2,4,5))

    return round(x+y+z)

def lineEq(stone: Stone) -> Line:
    (x1,y1,_), (dx,dy,_) = stone 
    x2, y2 = x1+dx, y1+dy 
    m = (y2-y1) / (x2-x1)
    b = y1 - (m * x1)
    return m, b

def intersectionPoint(eq1: Line, eq2: Line) -> Point|None:
    (a1, c1), (a2, c2) = eq1, eq2 
    b1, b2 = -1, -1 
    xnum = (b1*c2) - (b2*c1)
    ynum = (a2*c1) - (a1*c2)
    denom = (a1*b2) - (a2*b1)
    if denom == 0:
        return None 
    return (xnum / denom, ynum / denom)

def isFuturePoint(pt: Point, stone: Stone) -> bool:
    px, py = pt 
    (x,y,_), (dx,dy,_) = stone 
    ok1 = px > x if dx > 0 else px < x
    ok2 = py > y if dy > 0 else py < y 
    return ok1 and ok2

if __name__ == '__main__':
    do(solve, 23, 24)

'''
Part1:
- Read the position and velocity of each stone
- Compute the line equation of each stone: y=mx+b
    - Let x1, y1 = position of stone
    - Let dx, dy = velocity of stone 
    - Compute x2, y2 by adding x1+dx, y1+dy 
    - Compute slope (m): (y2 - y1) / (x2 - x1)
    - Compute intercept (b): y1 - (m * x1)
- Go through all pair combinations of stones:
    - Compute intersection point of two stones, if any
    - Convert the y = mx + b to ax + by + c = 0
    - Use equation to find intersection of two points:
        x = (b1*c2 - b2*c1) / (a1*b2 - a2*b1)
        y = (a2*c1 - a1*c2) / (a1*b2 - a2*b1)
    - Skip pair if no intersection point
    - Check if the point is inside the specified area
    - Check if intersection point is a future point (happens after the initial position) 
      of the two stones
    - Count number of pairs that has intersection point inside area and future point of both stones

Part2:
- Burnout, used a Reddit solution to complete AOC 2023
- Reference: https://www.reddit.com/r/adventofcode/comments/18pnycy/comment/ket7ajw/ 
'''