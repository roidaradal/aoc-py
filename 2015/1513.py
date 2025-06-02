# Advent of Code 2015 Day 13
# John Roy Daradal 

import itertools
from aoc import *
from graph import *

def data(full: bool) -> Graph:
    g = Graph()
    for line in readLines(15, 13, full):
        p = line.strip('.').split()
        a, b = p[0], p[-1]
        sign = 1 if p[2] == 'gain' else -1 
        w = int(p[3]) * sign 
        g.vertices.add(a)
        g.vertices.add(b)
        g.edges[(a,b)] = w
    return g 

def part1():
    g = data(full=True)
    vertices = sorted(g.vertices)
    head, rest = vertices[0], vertices[1:]
    maxScore = findBestSeating(head, rest, g.edges)
    print(maxScore)

def part2():
    g = data(full=True)
    head, rest = 'Me', list(g.vertices)
    maxScore = findBestSeating(head, rest, g.edges)
    print(maxScore)

def findBestSeating(head: str, rest: list[str], edges: EdgeMap) -> int:
    maxScore = -float('inf')
    for seating in itertools.permutations(rest):
        seating = (head,) + seating 
        maxScore = max(maxScore, computeScore(seating, edges))
    return int(maxScore)

def computeScore(seating: tuple[str,...], edges: EdgeMap) -> int:
    total = 0
    limit = len(seating)
    for i in range(limit):
        curr = seating[i]
        prev = seating[i-1]
        nxt = seating[(i+1) % limit]
        total += edges[(curr,prev)]
        total += edges[(curr,nxt)]
    return total

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Sort the vertices of the graph alphabetically (from set)
- Use the first person as the head of the table, the rest of the table will be the other vertices
- To find the best seating, find the permutations of the rest and add the head to the start (fixed)
- Compute the score of this seating arrangement:
    - For each person in the arrangement, add to the total the edge weight for its neighbors (next and previous)
    - For people at the ends, wrap-around: next of last = 0, prev of 0 = last
- Output the maximum score found

Part2:
- Similar to Part 1, but the head of the table is now Me 
- The rest of the table will now include all vertices
'''