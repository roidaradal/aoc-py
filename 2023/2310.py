# Advent of Code 2023 Day 10
# John Roy Daradal 

from aoc import *
from shapely.geometry import Point 
from shapely.geometry.polygon import Polygon

class Grid:
    def __init__(self):
        self.start: coords = (0,0)
        self.bounds: dims2 = (0,0)
        self.edges: dict[coords, list[coords]] = defaultdict(list)
        self.edgeCount: dict[tuple[coords,coords],int] = defaultdict(int)
    
    def addEdge(self, node1: coords, node2: coords):
        node1, node2 = sorted([node1, node2])
        pair = (node1, node2)
        self.edgeCount[pair] += 1
    
    def createEdges(self):
        edges: dict[coords, set] = defaultdict(set)
        for (node1, node2), count in self.edgeCount.items():
            if count != 2: continue 
            edges[node1].add(node2)
            edges[node2].add(node1)
        self.edges = {k: list(v) for k,v in edges.items()}

def data(full: bool) -> Grid:
    lines = readLines(23, 10, full)
    grid = Grid()
    grid.bounds = getBounds(lines)
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            c1 = (row,col)
            if char == '.': continue 
            dirs = []
            if char == '|':
                dirs = [U, D]
            elif char == '-':
                dirs = [L, R]
            elif char == 'L':
                dirs = [U, R]
            elif char == 'J':
                dirs = [U, L]
            elif char == '7':
                dirs = [L, D]
            elif char == 'F':
                dirs = [R, D]
            elif char == 'S':
                grid.start = c1 
                dirs = [U, D, L, R]
            for d in dirs:
                c2 = move(c1, d)
                if not insideBounds(c2, grid.bounds): continue 
                grid.addEdge(c1, c2)
    grid.createEdges()
    return grid

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    grid = data(full=True)
    maxDistance = bfsMaxDistance(grid)
    return maxDistance 

def part2() -> int:
    grid = data(full=True)
    points = dfsVisit(grid)
    polygon = Polygon(points)
    count = 0 
    rows,cols = grid.bounds 
    for row in range(rows):
        for col in range(cols):
            c = (row,col)
            if c in points: continue 
            point = Point(*c)
            if polygon.contains(point):
                count += 1
    return count 

def bfsMaxDistance(grid: Grid) -> int:
    dist: dict[coords, int] = {}
    visited: set[coords] = set()
    q: list[tuple[coords, coords|None]] = [(grid.start, None)]
    while len(q) > 0:
        node, prev = q.pop(0)
        d =  0
        if prev != None:
            d = dist[prev] + 1 
        dist[node] = d 
        visited.add(node)
        for node2 in grid.edges[node]:
            if node2 in visited: continue 
            q.append((node2, node))
    return max(dist.values())

def dfsVisit(grid: Grid) -> list[coords]:
    stack = [grid.start]
    points = []
    while len(stack) > 0:
        node = stack.pop()
        if node in points: continue 
        points.append(node)
        for node2 in grid.edges[node]:
            if node2 in points: continue
            stack.append(node2)
    return points

if __name__ == '__main__':
    do(solve, 23, 10)

'''
CreateGrid: 
- Process the grid to create the edges; skip . characters
- Depending on the direction of pipe, set up the directions to add edge 
- Keep track of the number of times a pair has been added as an edge
- Only keep pairs that have count == 2 (added both ways)

Part1:
- Using the grid and its edges, use BFS traversal to find the points reachable from the start
- For each visited node, keep track of the distance from start (1 + prev)
- Output the maximum distance value: the no. of steps farthest from the start

Part2:
- Using the grid and its edges, use DFS traversal to find the points that form the enclosing loop
- Use shapely.geometry library to form a polygon out of the points 
- For each point in the grid, excluding the points that form the enclosing loop, test if that point is inside polygon
- Output the number of points that are inside the polygon (enclosing loop)
'''