# Advent of Code 2021 Day 12
# John Roy Daradal 

from aoc import *

Edges = dict[str, list[str]]

def data(full: bool) -> Edges:
    edges: Edges = defaultdict(list)
    for line in readLines(21, 12, full):
        v1, v2 = splitStr(line, '-')
        if v2 != 'start': edges[v1].append(v2)
        if v1 != 'start': edges[v2].append(v1)
    return edges

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    edges = data(full=True)
    q: list[list[str]] = [['start']]
    count = 0
    while len(q) > 0:
        path = q.pop(0)
        last = path[-1]
        for node in edges[last]:
            if node.islower() and node in path: continue 
            if node == 'end':
                count += 1
            else:
                path2 = path[:] + [node]
                q.append(path2)
    return count 

def part2() -> int:
    edges = data(full=True)
    q: list[tuple[list[str], bool]] = [(['start'], False)]
    count = 0 
    while len(q) > 0:
        path, hasDouble = q.pop(0)
        last = path[-1]
        for node in edges[last]:
            willDouble = node.islower() and node in path 
            if hasDouble and willDouble: continue 
            if node == 'end':
                count += 1
            else:
                hasDouble2 = hasDouble or willDouble 
                path2 = path[:] + [node]
                q.append((path2, hasDouble2))
    return count

if __name__ == '__main__':
    do(solve, 21, 12)

'''
Part1:
- Use BFS to count valid paths from start-end
- Add to the queue by taking the last node of the path and checking its connected edges
- Skip if the next node is lowercase (small cave) and already in the path (cannot visit small caves twice)
- If next node is 'end', increment the path counter 
- Otherwise, extend the path with this next node and add to the queue

Part2:
- Similar to Part 1, but has extra flag to indicate if a small cave has already been visited twice in the path
- If already has a small cave visited twice, we cannot have another small cave visited twice 
'''