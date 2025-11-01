# Advent of Code 2023 Day 23
# John Roy Daradal 

from aoc import *

Grid = list[str]
Graph = dict[coords, set[int3]]

directions: dict[str, list[delta]] = {
    '.' : [U,D,L,R],
    'v' : [D],
    '>' : [R],
}

def data(full: bool) -> tuple[Grid, coords]:
    grid = readLines(23, 23, full)
    rows,cols = getBounds(grid)
    goal: coords = (rows-1, cols-2)
    return grid, goal

def solve() -> Solution:
    grid, goal = data(full=True)

    # Part 1 
    graph1 = buildGraph(grid, True)
    longest1 = findLongestPath(graph1, goal)

    # Part 2
    graph2 = buildGraph(grid, False)
    graph2 = mergeGraph(graph2)
    longest2 = findLongestPath(graph2, goal)

    return newSolution(longest1, longest2)

def buildGraph(grid: Grid, useSlope: bool) -> Graph:
    graph: Graph = defaultdict(set)
    bounds = getBounds(grid)
    for y, line in enumerate(grid):
        for x, tile in enumerate(line):
            if tile == '#': continue
            dirs = directions[tile] if useSlope else directions['.']
            curr = (y,x)
            for d in dirs:
                nxt = move(curr, d)
                ny,nx = nxt
                if not insideBounds(nxt, bounds): continue 
                if grid[ny][nx] == '#': continue 
                graph[(y,x)].add((ny, nx, 1))
    return graph

def findLongestPath(graph: Graph, goal: coords) -> int:
    stack: list[int3] = [(0, 1, 0)]
    visited = set()
    maxPath = 0 
    while len(stack) > 0:
        y, x, score = stack.pop()
        curr = (y,x)
        if score == -1:
            visited.remove(curr)
            continue 
        if curr == goal:
            maxPath = max(maxPath, score)
            continue 
        if curr in visited: continue 
        visited.add(curr)

        stack.append((y, x, -1))
        for ny, nx, w in graph[curr]:
            stack.append((ny, nx, score+w))
    return maxPath

def mergeGraph(graph: Graph) -> Graph:
    while True:
        for node, edges in graph.items():
            if len(edges) == 2:
                (ay, ax, aw), (by, bx, bw) = edges 
                graph[(ay,ax)].remove(node + (aw,))
                graph[(by,bx)].remove(node + (bw,))
                graph[(ay,ax)].add((by, bx, aw+bw))
                graph[(by,bx)].add((ay, ax, aw+bw))
                del graph[node]
                break
        else:
            break
    return graph

if __name__ == '__main__':
    do(solve, 23, 23)

'''
Part1:
- Build the connection graph from the grid, with slopes enabled:
    - Go through grid tiles, skipping walls (#)
    - For normal tiles, look at its 4 neighbors (UDLR)
    - For slope tiles (>v), only consider the slope direction
    - Add edge from current coordinate to neighbor, with weight=1
- Use DFS to find the longest path from the graph
- Start at (0,1) with pathLength = 0
- Slight modification to the DFS to find longest path:
    - After ensuring that current (y,x) is not yet visited, add the (y,x) to top of stack with score=-1
    - Then, we add its graph neighbors to the stack, with score = score + edge weight 
    - After processing all neighbors, we will have to pop off the (y,x) previously pushed with score of -1
    - We remove it from visited set

Part2:
- Build the connection graph from the grid, without slopes
- For slope tiles, use all 4 directions as if it were a normal tile (.)
- Compress the graph to make it smaller:
    - For nodes with only 2 edges, remove the node from the graph and connect the 2 neighbors instead
    - Remove the old node from the 2 neighbor's edge sets
    - Add the neighbors to each other's edge sets, with the combined weight of the 2 old edges
    - Repeat until no more nodes with only 2 neighbors
- Use the DFS from Part 1 to find the longest path on the compressed graph
'''