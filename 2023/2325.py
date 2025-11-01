# Advent of Code 2023 Day 25
# John Roy Daradal 

from aoc import *

Connection = tuple[str, set[str]]

def data(full: bool) -> list[Connection]:
    connections: list[Connection] = []
    for line in readLines(23, 25, full):
        key, tail = splitStr(line, ':')
        group = set(splitStr(tail, None))
        connections.append((key, group))
    return connections

def solve() -> Solution:
    connections = data(full=True)

    # Create the edges and collect the unique nodes
    edges: dict[str, set[str]] = defaultdict(set)
    vertices: set[str] = set()
    for node1, nodes in connections:
        vertices.add(node1)
        for node2 in nodes:
            edges[node1].add(node2)
            edges[node2].add(node1)
            vertices.add(node2)

    # Get the APSP through BFS
    # Tally how much each edge was used in the shortest paths
    edgeCounts: dict[str2, int] = defaultdict(int)
    for node in vertices:
        paths = bfsShortestPath(node, edges)
        for path in paths.values():
            limit = len(path)
            if limit == 1: continue 
            for i in range(1, limit):
                n1, n2 = sorted([path[i-1], path[i]])
                edge: str2 = (n1, n2)
                edgeCounts[edge] += 1

    # Top 3 most used edge = cut set
    entries = [(count, edge) for edge,count in edgeCounts.items()]
    entries.sort(reverse=True)
    # Remove the 3 edges
    for _, (node1,node2) in entries[0:3]:
        edges[node1].remove(node2)
        edges[node2].remove(node1)
    node1, node2 = entries[0][1]
    group1 = bfsShortestPath(node1, edges)
    group2 = bfsShortestPath(node2, edges)
    size1, size2 = len(group1), len(group2)
    product = size1 * size2

    return newSolution(product,'')

def bfsShortestPath(start: str, edges: dict[str, set[str]]) -> dict[str, list[str]]:
    sp: dict[str, list[str]] = {}
    q: list[list[str]] = [[start]]
    while len(q) > 0:
        path = q.pop(0)
        node1 = path[-1]
        if node1 in sp: continue
        sp[node1] = path

        for node2 in edges[node1]:
            if node2 in sp: continue
            q.append(path + [node2])
    return sp

if __name__ == '__main__':
    do(solve, 23, 25)

'''
Solve:
- Create the undirected edges and collect the unique set of nodes from the graph
- With each node as the starting point, use BFS to find the shortest path to other nodes
- For each shortest path, process the edge pairs that make up the path
- Tally how much each edge was used in the shortest paths 
- The top 3 most used edges should be the cut-set
- Idea: these are the frequently used because they are required for traversing from componentA to componentB
- Remove the top 3 edges from the graph
- Use BFS again to find the component sizes of group1 and group2 
- Output the product of the component sizes
- No problem for Part 2
'''