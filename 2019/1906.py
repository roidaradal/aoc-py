# Advent of Code 2019 Day 06
# John Roy Daradal 

from aoc import *

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.parentOf = {}

def data(full: bool) -> Graph:
    g = Graph()
    for line in readLines(19, 6, full):
        node,child = line.split(')')
        g.nodes.add(node)
        g.nodes.add(child)
        g.edges[node].append(child)
        g.edges[child].append(node)
        g.parentOf[child] = node
    return g

def solve() -> Solution:
    g = data(full=True)
    
    # Part 1
    total = bfs(g, 'COM', None)

    # Part 2 
    start = g.parentOf['YOU']
    goal  = g.parentOf['SAN']
    depth = bfs(g, start, goal)

    return newSolution(total, depth)

def bfs(g: Graph, start: str, goal: str|None) -> int:
    visited = {}
    q = [(start,0)]
    while len(q) > 0:
        node, depth = q.pop(0)
        if node in visited: continue 
        visited[node] = depth 
        if goal != None and node == goal:
            return depth 
        for node2 in g.edges[node]:
            if node2 in visited: continue 
            q.append((node2, depth+1))
    total = sum(visited.values())
    return total

if __name__ == '__main__':
    do(solve, 19, 6)

'''
Part1:
- Count of direct and indirect orbits of an object = depth in the graph
- Use BFS to find each object's depth
- Output the total depth of all objects

Part2:
- Start from the parent of YOU and the goal is parent of SAN
- Use BFS to traverse and find the shortest path from start to goal 
- Output the min number of steps needed to get there
'''