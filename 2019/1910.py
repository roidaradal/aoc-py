# Advent of Code 2019 Day 10
# John Roy Daradal 

import itertools
from aoc import *

def data(full: bool) -> tuple[list[coords], dims2]:
    lines = readLines(19, 10, full)
    asteroids = []
    rows, cols = len(lines), 0
    for row,line in enumerate(lines):
        cols = len(line)
        for col,char in enumerate(line):
            if char == '#': asteroids.append((row,col))
    return asteroids, (rows,cols)

def solve():
    asteroids, (rows,cols) = data(full=True)

    # Part 1
    visible = {a1: {a2: False for a2 in asteroids} for a1 in asteroids}
    sameRow: dict[int,set[coords]] = defaultdict(set)
    sameCol: dict[int,set[coords]] = defaultdict(set)
    sameLine: dict[tuple[float,float],set[coords]] = defaultdict(set)
    for a1,a2 in itertools.combinations(asteroids, 2):
        (y1,x1),(y2,x2) = a1, a2 
        if y1 == y2: # same row 
            sameRow[y1].add(a1)
            sameRow[y1].add(a2)
        elif x1 == x2: # same col 
            sameCol[x1].add(a1)
            sameCol[x1].add(a2)
        else: # compute y = mx + b
            mb = lineEq(a1, a2)
            sameLine[mb].add(a1)
            sameLine[mb].add(a2)
    
    oneRow: dict[int,list[coords]] = {}
    oneCol: dict[int,list[coords]] = {}
    oneLine: dict[tuple[float,float],list[coords]] = {}
    for row in sameRow:
        oneRow[row] = sorted(sameRow[row], key=lambda x: x[1])
    for col in sameCol:
        oneCol[col] = sorted(sameCol[col], key=lambda x: x[0])
    for mb in sameLine:
        oneLine[mb] = sorted(sameLine[mb], key=lambda x: x[1])

    lines = []
    lines.extend(oneRow.values())
    lines.extend(oneCol.values())
    lines.extend(oneLine.values())
    for points in lines:
        for i in range(len(points)-1):
            a1, a2 = points[i], points[i+1]
            visible[a1][a2] = True 
            visible[a2][a1] = True 
    
    scores = []
    for a in asteroids:
        score = sum(1 for ok in visible[a].values() if ok)
        scores.append((score, a))
    maxScore, (y,x) = max(scores)
    print(maxScore)

    # Part 2
    station = (y,x)

    hrzn = oneRow.get(y, [])
    vert = oneCol.get(x, [])
    diag = sorted((mb[0],pts) for mb,pts in oneLine.items() if station in pts)
    ndiag = [pts for m,pts in diag if m < 0] # negative slope
    pdiag = [pts for m,pts in diag if m > 0] # positive slope

    goal = 200
    destroyed = []
    quadrant = 1 
    while len(destroyed) < goal:
        if quadrant == 1:
            idx = vert.index(station)
            if idx > 0:
                a = vert[idx-1]
                if a not in destroyed: destroyed.append(a)
                del vert[idx-1]
            for pts in ndiag:
                idx = pts.index(station)
                if idx == len(pts)-1: continue # skip if last 
                a = pts[idx+1]
                if a not in destroyed: destroyed.append(a)
                del pts[idx+1]
            quadrant = 2
        elif quadrant == 2:
            idx = hrzn.index(station)
            if idx < len(hrzn)-1:
                a = hrzn[idx+1]
                if a not in destroyed: destroyed.append(a)
                del hrzn[idx+1]
            for pts in pdiag:
                idx = pts.index(station)
                if idx == len(pts)-1: continue # skip if last 
                a = pts[idx+1]
                if a not in destroyed: destroyed.append(a)
                del pts[idx+1]
            quadrant = 3
        elif quadrant == 3:
            idx = vert.index(station)
            if idx < len(vert)-1: 
                a = vert[idx+1]
                if a not in destroyed: destroyed.append(a)
                del vert[idx+1]
            for pts in ndiag:
                idx = pts.index(station)
                if idx == 0: continue # skip if first 
                a = pts[idx-1]
                if a not in destroyed: destroyed.append(a)
                del pts[idx-1]
            quadrant = 4
        elif quadrant == 4:
            idx = hrzn.index(station)
            if idx > 0:
                a = hrzn[idx-1]
                if a not in destroyed: destroyed.append(a)
                del hrzn[idx-1]
            for pts in pdiag:
                idx = pts.index(station)
                if idx == 0: continue # skip if first 
                a = pts[idx-1]
                if a not in destroyed: destroyed.append(a)
                del pts[idx-1]
            quadrant = 1

    y,x = destroyed[goal-1]
    print((x*100) + y)

def lineEq(a1: coords, a2: coords) -> tuple[float,float]:
    a1, a2 = sortX(a1, a2)
    (y1,x1),(y2,x2) = a1, a2 
    m = (y2-y1) / (x2-x1)
    b = y1 - (m*x1)
    return m, b

def sortX(a1: coords, a2: coords) -> tuple[coords, coords]:
    a1, a2 = sorted([a1, a2], key=lambda x: x[1]) # sort by x 
    return a1, a2 

if __name__ == '__main__':
    do(solve)

'''
Part1:
- Initialize pairwise visibility of asteroids to all False
- Go through each pair of asteroids 
- Check if asteroids are in same row or same column 
- If not, compute the line equation (y = mx+b) that will align these two
- Sort the points in one row (by x), one column (by y) and one line (by x)
- Go through all the list of points after sorting; process each successive pairs
- If two asteroids are in one row/column/line and successive, they are visible to each other
- For each asteroid, compute the number of visible asteroids 
- Output the max score and the coords of that asteroid (for Part 2)

Part2:
- Choose station with max score from Part 1
- Get its horizontal line (one row), vertical line (one col), 
  and lines where it is a part of (ndiag = negative slope, pdiag = positive slope)
- Destroy at least 200 asteroids, starting from quadrant 1 
- In Q1, start with VERT, destroy above station 
  Go through negative slopes in ascending order, destroy asteroid after station 
- In Q2, start with HRZN, destroy after station 
  Go through positive slopes in ascending order, destroy asteroid after station 
- In Q3, start with VERT, destroy below station 
  Go through negative slopes in ascending order, destroy asteroid before station
- In Q4, start with HRZN, destroy before station
  Go through positive slopes in ascending order, destroy asteroid before station
- After finishing a quadrant, go to the next quadrant, looping back from Q4 to Q1 
- Output the 200th asteroid destroyed's x coord * 100 + y
'''