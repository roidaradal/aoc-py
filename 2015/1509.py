# Advent of Code 2015 Day 09
# John Roy Daradal 

import itertools
from aoc import *
from graph import *

def data(full: bool) -> Graph:
    g = Graph()
    for line in readLines(15, 9, full):
        head, tail = splitStr(line, '=')
        w = int(tail)
        v1,v2 = splitStr(head,'to')
        g.vertices.add(v1)
        g.vertices.add(v2)
        g.edges[(v1,v2)] = w 
        g.edges[(v2,v1)] = w
    return g

def solve():
    g = data(full=True)
    minDistance = float('inf')
    maxDistance = 0
    for path in itertools.permutations(g.vertices):
        distance = computeDistance(path, g.edges)
        minDistance = min(minDistance, distance)
        maxDistance = max(maxDistance, distance)
    print(minDistance) 
    print(maxDistance)

def computeDistance(path: tuple, edges: EdgeMap) -> int:
    indexes = list(range(1, len(path)))
    fn = lambda i: edges[(path[i-1], path[i])]
    return getTotal(indexes, fn)

if __name__ == '__main__':
    do(solve)

'''
Solve:
- For Part 1, find the min distance; for Part 2, find the max distance
- Enumerate all possible paths by using permutations of graph vertices 
- For each path, compute the path distance by getting the total edge weights of all adjacent vertices in the path
'''