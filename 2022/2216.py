# Advent of Code 2022 Day 16
# John Roy Daradal 

import itertools
from aoc import *

Valves = tuple[str,...]
IntMap = dict[str, int]
Edges  = dict[str, list[str]]
Graph  = dict[str, dict[str, int]]
State  = tuple[str, list[str], int, int] # current, openValves, minutesLeft, score

def data(full: bool) -> tuple[IntMap, Edges]:
    flowRate : IntMap = {}
    edges: Edges = {}
    for line in readLines(22, 16, full):
        for rep in (';', ',', 'rate='): line = line.replace(rep, '')
        p = splitStr(line, None)
        name = p[1]
        rate = int(p[4])
        flowRate[name] = rate 
        edges[name] = p[9:]
    return flowRate, edges

def solve() -> Solution:
    flowRate, edges = data(full=True)
    start = 'AA'
    graph = buildGraph(flowRate, edges, start)

    # Part 1
    flow1 = findMaxFlow(graph, flowRate, start, 30)
    maxFlow = max(flow1.values())

    # Part 2
    flow2 = findMaxFlow(graph, flowRate, start, 26)
    entries = [(flow, opened) for opened, flow in flow2.items()]
    maxTotal = 0
    for (total1, open1), (total2, open2) in itertools.combinations(entries, 2):
        if len(set(open1).intersection(set(open2))) > 0: continue # skip overlapping 
        maxTotal = max(maxTotal, total1+total2)

    return newSolution(maxFlow, maxTotal)

def bfsShortestPath(start: str, edges: Edges) -> IntMap:
    sp: IntMap = {}
    q: list[strInt] = [(start, 0)]
    while len(q) > 0:
        node, steps = q.pop(0)
        if node in sp: continue 
        sp[node] = steps 
        for nxt in edges[node]:
            if nxt in sp: continue 
            q.append((nxt, steps+1))
    return sp

def buildGraph(flowRate: IntMap, edges: Edges, start: str) -> Graph:
    graph: Graph = {}
    for node1 in edges:
        # skip 0-flow nodes that are not the starting node 
        if flowRate[node1] == 0 and node1 != start: continue
        graph[node1]= {}
        for node2, steps in bfsShortestPath(node1, edges).items():
            if flowRate[node2] == 0 and node2 != start: continue 
            if node1 == node2 and node1 == start: continue
            graph[node1][node2] = steps + 1 # steps to travel, 1 to open
    return graph

def findMaxFlow(graph: Graph, flowRate: IntMap, start: str, minutes: int) -> dict[Valves, int]:
    maxFlow: dict[Valves, int] = defaultdict(int)
    stack: list[State] = [(start, [], minutes, 0)]
    while len(stack) > 0:
        curr, opened, minutes, prevScore = stack.pop()
        key: Valves = tuple(sorted(opened))

        # Compute current flow from the open valves 
        currFlow = sum(flowRate[v] for v in opened)

        # Option 1: Stay here until time expires
        maxFlow[key] = max(maxFlow[key], prevScore + (minutes * currFlow))

        # Option 2: Continue exploring closed neighbors 
        for nxt, steps in graph[curr].items():
            if nxt in opened: continue # skip opened neighbor
            if nxt == start: continue  # don't go back to starting point 
            if minutes < steps: continue # unreachable
            nxtScore = prevScore + (steps * currFlow)
            stack.append((nxt, opened + [nxt], minutes - steps, nxtScore))

    return maxFlow

if __name__ == '__main__':
    do(solve, 22, 16)

'''
Part1:
- Use BFS starting at each node to compute the All-Pairs Shortest Paths
- Create a compressed graph, without the 0-flow nodes that are not the starting node AA 
- Use the APSP values for the edge weight between node1 and node2 + add 1 (cost to open valve)
- Find the max flow on the new graph for 30 minutes
- Use DFS to explore all possible ways to open the valves to find the maximum flow possible 
- The stack states consist of (currentNode, openValves, minutesLeft, currentScore)
- Keep track of the maximum flow possible for all encountered openValves combination
- When we examine a state, compute the total flow from the open valves
- First option is we stay here until time expires (stop exploration)
    - Update the maxFlow for this openValve config: the totalFlow we will get if we stay here 
      will be prevScore + (minutesLeft * currentFlow)
- Second option is to explore neighbors whose valves are still closed:
    - We skip current node's neighbors that are open or the starting node AA
    - We also skip if the steps it takes to reach the neighbor exceeds the minutesLeft (unreachable)
    - Add the next state to the stack: at nextNode, opened valves will include the nextNode, 
      minutesLeft - steps going to neighbor, nextScore = prevScore + (steps * current flow)
- Return the maximum flow value found

Part2:
- We use the same findMaxFlow function from Part 1, but only using 26 minutes
- Since the function returns the maximum flow possible for all openValve configuration encountered, 
  we will check the combinations of these openValve configs to find a non-overlapping pair that maximizes the total
- Idea: Instead of finding the path for you and the elephant simultaneously, we can instead think of it as 
  you opening the valves for 26 minutes, then the elephant will traverse for 26 minutes, but avoiding the valves 
  you already opened previously, as this wont add more flow 
- For all pair combinations of openValve configs, skip the pairs with overlapping open valves 
- Return the maximum sum of flows from the pairs
'''