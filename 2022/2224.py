# Advent of Code 2022 Day 24
# John Roy Daradal 

import heapq
from aoc import *

Blizzards = dict[delta, list[coords]]

firstRow, firstCol = 1, 1
lastRow, lastCol = 0, 0

def data(full: bool) -> Blizzards:
    global lastRow, lastCol
    T: dict[str, delta] = {
        '>' : R,
        '<' : L, 
        '^' : U,
        'v' : D,
    }
    blizzards: Blizzards = defaultdict(list)
    grid = readLines(22, 24, full)
    for row, line in enumerate(grid):
        for col, tile in enumerate(line):
            if tile not in T: continue
            blizzards[T[tile]].append((row,col))
    rows, cols = getBounds(grid)
    lastRow, lastCol = rows-2, cols-2
    return blizzards

def solve() -> Solution:
    blizzards = data(full=True)
    start: coords = (firstRow-1, firstCol)
    goal: coords = (lastRow+1, lastCol)

    # Part 1
    path1, blizzards1 = findShortestPath(start, goal, blizzards)

    # Part 2
    path2, blizzards2 = findShortestPath(goal, start, blizzards1)
    path3, _          = findShortestPath(start, goal, blizzards2)
    total = path1 + path2 + path3

    return newSolution(path1, total)

def findShortestPath(start: coords, goal: coords, blizzards: Blizzards) -> tuple[int, Blizzards]:
    state: dict[int, Blizzards] = {}
    danger: dict[int, set[coords]] = {}
    state[0] = blizzards 
    danger[0] = getDangerZones(blizzards)

    sp: dict[coords, dict[int,int]] = defaultdict(lambda: defaultdict(lambda: sys.maxsize))
    pq: list[tuple[int,coords]] = []
    heapq.heappush(pq, (0, start))

    while len(pq) > 0:
        minute, curr = heapq.heappop(pq)

        nxtMinute = minute + 1 
        if nxtMinute not in state:
            state[nxtMinute] = nextState(state[minute])
            danger[nxtMinute] = getDangerZones(state[nxtMinute])

        # Check next positions or stay at current position 
        nxtPositions: list[coords] = []
        for ny,nx in surround4(curr) + [curr]:
            nxt = (ny,nx)
            if nx < firstCol or nx > lastCol: continue 
            if ny < firstRow and nxt not in (start, goal): continue 
            if ny > lastRow and nxt not in (start, goal): continue 
            if nxt in danger[nxtMinute]: continue 
            nxtPositions.append(nxt)

        currentBestSP = getCurrentBest(sp[goal])
        for nxt in nxtPositions:
            bestPossible = nxtMinute + manhattan(nxt, goal)
            if bestPossible > currentBestSP: continue # skip if cannot be better than current best
            if sp[nxt][nxtMinute] > nxtMinute:
                sp[nxt][nxtMinute] = nxtMinute
                heapq.heappush(pq, (nxtMinute, nxt))

    minPath = min(sp[goal].keys())
    return minPath, state[minPath]

def getDangerZones(blizzards: Blizzards) -> set[coords]:
    danger: set[coords] = set()
    for positions in blizzards.values():
        danger = danger.union(set(positions))
    return danger

def getCurrentBest(sp: dict[int,int]) -> int:
    choices: list[int] = [sys.maxsize]
    for minute in sp.keys():
        choices.append(minute)
    return min(choices)

def nextState(blizzards: Blizzards) -> Blizzards:
    blizzards2: Blizzards = defaultdict(list)
    for d in blizzards:
        for y,x in blizzards[d]:
            ny, nx = move((y,x), d)
            if d == U and y == firstRow:
                ny = lastRow
            elif d == D and y == lastRow:
                ny = firstRow 
            elif d == L and x == firstCol:
                nx = lastCol 
            elif d == R and x == lastCol:
                nx = firstCol
            blizzards2[d].append((ny, nx))
    return blizzards2

if __name__ == '__main__':
    do(solve, 22, 24)

'''
Solve:
- Get the initial blizzard positions, grouped by their directions, from the input 
- Create the starting and goal positions: (0,1) and (rows-1,cols-2)
- Use modified Dijkstra's algorithm to find the shortest path from start to goal
    - At each point, they can arrive using multiple minutes
    - For next states, check the 4 neighbors (UDLR) for the next minute
    - If your next position hits a wall or hits a blizzard, skip it
    - Get the current best shortest path at the goal
    - For each next position, check if their best possible (nxtMinute + Manhattan distance to the goal)
      can improve the current best; if not, skip it (pruning)
    - If the sp[nxtPosition][nxtMinute] > nxtMinute, update it and add to the priority queue
    - Return the minimum minute at the goal, and the state of blizzards at that minute
- Keep track of the blizzard positions (union of positions = danger zones) at each minute (cached)
    - The blizzard positions at minute 0 is the given initial blizzard positions
    - Compute the next state of blizzards if not yet in cache
    - A blizzard moves in its given direction, but if it hits a wall, it continues on the other side 
      with the same direction:
        - If going up and already at first row, next blizzard appears at last row
        - If going down and already at last row, next blizzard appears at first row
        - If going left and already at first col, next blizzard appears at last col
        - If going right and already at last col, next blizzard appears at first col
- For Part 1, find the shortest path from start to goal
- For Part 2, find the shortest path from start -> goal, goal -> start, start -> goal
    - Reuse the solution from Part 1; starting blizzard for next round is ending blizzard when we reached the goal
    - Find the shortest path from goal to start, using the ending blizzard from previous round as the starting blizzard
    - Find the shortest path from start to goal, using the ending blizzard from previous round as the starting blizzard
    - Get the total of path1, path2, and path3
'''