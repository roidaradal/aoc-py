# Advent of Code 2025 Day 11
# John Roy Daradal 

from aoc import *

Graph = dict[str, list[str]]

def data(full: bool) -> Graph:
    graph: Graph = {}
    for line in readLines(25, 11, full):
        p = [x.strip() for x in line.split(':')]
        graph[p[0]] = [x.strip() for x in p[1].split()]
    return graph

def solve() -> Solution:
    graph = data(full=True)

    # Part 1 
    count1 = countPaths(graph, 'you', 'out')

    # Part 2
    allPaths = [
        [('svr', 'fft'), ('fft', 'dac'), ('dac', 'out')],
        [('svr', 'dac'), ('dac', 'fft'), ('fft', 'out')],
    ]
    count2 = 0
    for paths in allPaths:
        count = 1
        for start, end in paths:
            count *= countPaths(graph, start, end)
            if count == 0: break 
        count2 = max(count2, count)

    return newSolution(count1, count2)

def countPaths(graph: Graph, start: str, end: str) -> int:
    total = 0
    curr: dict[str, int] = {start: 1}
    while len(curr) > 0:
        nxt: dict[str, int] = defaultdict(int)
        for node, count in curr.items():
            if node == end:
                total += count 
            else:
                for node2 in graph.get(node, []):
                    nxt[node2] += count 
        curr = nxt
    return total

if __name__ == '__main__':
    do(solve, 25, 11)

'''
Part1:
- Count the number of paths from 'you' to 'out'
- Group paths together by only keeping track of the current node and how many
  paths it took to get there
- Start with starting node with count = 1
- Repeat until no more nodes to process:
    - Build the next map by checking the current map
    - If node is the end node, increment the total by the node path count 
    - Otherwise, for each of the node's neighbors, add them to the next map, 
      incrementing it by count (grouping similar nodes together)

Part2:
- Count the number of paths from 'svr' to 'out', but also needs to pass through 
  the nodes 'fft' and 'dac' (in any order)
- Break up the paths: svr => fft => dac => out and svr => dac => fft => out
- Count the number of paths for each fragment
- Once one fragment already becomes zero, we stop for this path (result already 0)
- Multiply the number of paths for each fragment = total number of paths
'''