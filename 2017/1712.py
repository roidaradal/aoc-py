# Advent of Code 2017 Day 12
# John Roy Daradal 

from aoc import *

def data(full: bool) -> dict[int, list[int]]:
    edges: dict[int, list[int]] = {}
    for line in readLines(17, 12, full):
        head, tail = splitStr(line, '<->')
        edges[int(head)] = toIntList(tail, ',')
    return edges

def solve() -> Solution:
    edges = data(full=True)

    # Part 1
    visited = findGroup(edges, 0)
    numVisited = len(visited)

    # Part 2
    group = {}
    groupID = 0 
    for node in sorted(edges.keys()):
        if node in group: continue 
        visited = findGroup(edges, node)
        for n in visited:
            group[n] = groupID 
        groupID += 1
    numGroups = len(set(group.values()))
    
    return newSolution(numVisited, numGroups)

def findGroup(edges: dict[int, list[int]], start: int) -> set[int]:
    visited: set[int] = set()
    q: list[int] = [start]
    while len(q) > 0:
        n = q.pop(0)
        if n in visited: continue 
        visited.add(n)
        for n2 in edges.get(n, []):
            if n2 in visited: continue 
            q.append(n2)
    return visited

if __name__ == '__main__':
    do(solve, 17, 12)

'''
Solve: 
- For Part 1, use BFS traversal to find the connected component of 0
- For Part 2, go through each node and find it's connected component
- Skip nodes that are already part of another group
- Output the number of groups found
'''