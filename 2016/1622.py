# Advent of Code 2016 Day 22
# John Roy Daradal 

import itertools
from aoc import *

USED, AVAIL = 0, 1
Grid = dict[coords, int2]

def data(full: bool) -> Grid:
    fs: Grid = {}
    lines = readLines(16, 22, full)
    for line in lines[2:]:
        for rep in 'xyT%': line = line.replace(rep, '')
        p = splitStr(line, None)
        h = splitStr(p[0], '-')
        x,y = int(h[1]), int(h[2])
        fs[(y,x)] = (int(p[2]), int(p[3]))
    return fs

def solve() -> Solution:
    fs = data(full=True)

    # Part 1
    count1 = 0
    for node1, node2 in itertools.combinations(fs.keys(), 2):
        for a,b in [(node1,node2), (node2, node1)]:
            usedA = fs[a][USED]
            availB = fs[b][AVAIL]
            if usedA > 0 and usedA <= availB:
                count1 += 1

    # Part 2
    ys = [c[0] for c in fs.keys()]
    xs = [c[1] for c in fs.keys()]
    ymax, xmax = max(ys), max(xs)
    bounds = (ymax+1, xmax+1)

    curr: coords = (0, xmax)
    goal: coords = (0, 0)
    size = fs[curr][USED]
    
    count2 = 0
    path = bfsShortestPath(fs, bounds, curr, goal, size)
    for dest in path[1:]:
        transferPath = bfsShortestPath(fs, bounds, dest, curr)
        count2 += transferData(fs, transferPath)

        fs[curr] = (0, fs[curr][AVAIL] + size)
        fs[dest] = (size, fs[dest][AVAIL] - size)
        count2 += 1
        curr = dest 

    return newSolution(count1, count2)

def bfsShortestPath(fs: Grid, bounds: dims2, pos1: coords, pos2: coords, size: int=0) -> list[coords]:
    transferMode = size == 0
    q: list[list[coords]] = [[pos1]]
    visited: set[coords] = set()
    while len(q) > 0:
        path = q.pop(0)
        curr = path[-1]
        currUsed = fs[curr][USED]
        if transferMode:
            if currUsed == 0: return path[::-1] # reversed path
        else: # goal mode
            if curr == pos2: return path

        if curr in visited: continue 
        visited.add(curr)

        for nxt in surround4(curr):
            if not insideBounds(nxt, bounds): continue 
            if nxt in visited: continue
            # skip if total size cannot fit the transferSize
            if transferMode:
                if nxt == pos2: continue # taboo node
                if sum(fs[nxt]) < currUsed: continue 
            else:
                if sum(fs[nxt]) < size: continue 
            q.append(path + [nxt])

    return []

def transferData(fs: Grid, path: list[coords]) -> int: 
    numTransfers = len(path)-1
    for i in range(numTransfers):
        curr, prev = path[i], path[i+1]
        prevUsed = fs[prev][USED]
        fs[curr] = (prevUsed, fs[curr][AVAIL] - prevUsed)
        fs[prev] = (0, fs[prev][AVAIL] + prevUsed)
    return numTransfers

if __name__ == '__main__':
    do(solve, 16, 22)

'''
Part1:
- The filesystem grid is made up of nodes, where each node is represented by (usedSpace, availableSpace)
- Go through all pair combinations of nodes
- For each pair, expand into (A,B) and (B,A) arrangement of the 2 nodes
- Count the pairs where A[USED] > 0 and A[USED] <= B[AVAIL]: A is not empty and A can fit inside B's available space

Part2:
- Starting from the top-right corner (0,xmax), transfer the data here to the node in (0,0)
- Use BFS to find the shortest path from (0,xmax) to (0,0), where all the nodes in the path can fit 
  the size of the data at (0,xmax) => total space of node (used + avail) >= size
- For each node in the path (except the start at (0,xmax)), empty out its contents first so we can move the data from 
  the previous node onto here
- Use BFS to find the shortest path from the current destination node to the blank node (USED = 0); 
  we will send the current node (the one holding the data) as a taboo node, for it not to be included in the path
- All nodes in the shortest path in transfer mode should have total size >= previous node's used space,
  since we will be transferring all of the data backwards
- When we find the blank node (used = 0), return the reversed path (since we'll process it from blank node first)
- From the found path (blank node -> destination node), transfer the contents of the previous node 
  to the current node, updating the nodes' available and used sizes
- The result is destination node will now be empty, ready for transfer of the data from current node
- The number of steps to clear out the destination node = len(path)-1; we add this to the total step count 
- We can now transfer the data from current -> destination node, adding 1 step to the process
- Update the current node as the previous destination node, and repeat the process until we reach the (0,0) node - 
  the last node in the path from the first BFS above
'''