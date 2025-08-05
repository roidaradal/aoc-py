# Advent of Code 2018 Day 25
# John Roy Daradal 

import itertools
from aoc import *

def data(full: bool) -> list[int4]:
    def fn(line: str) -> int4:
        a,b,c,d = toIntList(line, ',')
        return (a,b,c,d)
    return [fn(line) for line in readLines(18, 25, full)]

def solve() -> Solution:
    points: list[int4] = data(full=True)

    # Create graph: add edge between points if manhattan <= 3
    edges: dict[int4, list[int4]] = defaultdict(list)
    for p1, p2 in itertools.combinations(points, 2):
        if manhattan4(p1, p2) <= 3:
            edges[p1].append(p2)
            edges[p2].append(p1)

    groupOf: dict[int4, int] = {}
    group = 0
    for pt in points:
        if pt in groupOf: continue 
        connected = bfsTraverse(edges, pt)
        for pt2 in connected:
            groupOf[pt2] = group
        group += 1

    return newSolution(group, "")

def manhattan4(p1: int4, p2: int4=(0,0,0,0)) -> int:
    return sum(abs(p1[i]-p2[i]) for i in range(4))

def bfsTraverse(edges: dict[int4, list[int4]], start: int4) -> set[int4]:
    visited: set[int4] = set()
    q: list[int4] = [start]
    while len(q) > 0:
        curr = q.pop(0)
        if curr in visited: continue 
        visited.add(curr)
        for nxt in edges[curr]:
            if nxt in visited: continue 
            q.append(nxt)
    return visited

if __name__ == '__main__':
    do(solve, 18, 25)

'''
Solve:
- For each pair of points, add an edge between them if their Manhattan distance <= 3
- Go through each point: use them as starting point for BFS traversal to find the 
  constellation that contains this starting point
- If a point already has been included in a previous group, skip it
- Output the number of groups formed by the points
- No problem for Part 2
'''