# Advent of Code 2024 Day 16
# John Roy Daradal 

import heapq
from aoc import *

Grid = list[str]
State = tuple[coords, delta, int, list[coords]]
Pair = tuple[coords, delta]

def data(full: bool) -> tuple[Grid, coords, coords]:
    grid = readLines(24, 16, full)
    start: coords = (0,0)
    goal: coords = (0,0)
    for row, line in enumerate(grid):
        for col, tile in enumerate(line):
            if tile == 'S':
                start = (row,col)
            elif tile == 'E':
                goal = (row,col)
    return grid, start, goal

def solve() -> Solution:
    grid, start, goal = data(full=True)

    # Initialize shortest path tables
    rows, cols = getBounds(grid)
    sp: dict[coords, dict[delta, int]] = {}
    prev: dict[coords, dict[delta, list[Pair]]] = {}
    for r in range(rows):
        for c in range(cols):
            sp[(r,c)] = defaultdict(lambda: sys.maxsize)
            prev[(r,c)] = defaultdict(list)
    
    # Part 1
    pq: list[tuple[int,coords,delta]] = []
    heapq.heappush(pq, (0, start, R))
    while len(pq) > 0:
        total, curr, d = heapq.heappop(pq)
        nxtStates: list[tuple[coords, delta, int]] = []

        # Turn left/right and move forward
        for turn in [leftOf, rightOf]:
            d2 = turn[d]
            nxt = move(curr, d2)
            nxtStates.append((nxt, d2, 1001))

        # Move forward in current direction 
        nxt = move(curr, d)
        nxtStates.append((nxt, d, 1))

        for nxt, d2, cost in nxtStates:
            ny,nx = nxt 
            if grid[ny][nx] == '#': continue

            total2 = total + cost
            if sp[nxt][d2] >= total2:
                if sp[nxt][d2] > total2:
                    prev[nxt][d2] = [] # reset list 
                prev[nxt][d2].append((curr, d))
                sp[nxt][d2] = total2 
                heapq.heappush(pq, (sp[nxt][d2], nxt, d2))

    goalEntries = [(v,d) for d,v in sp[goal].items()]
    minPath, minDelta = min(goalEntries)

    # Part 2 
    q: list[Pair] = [(goal, minDelta)]
    visited: set[Pair] = set()
    while len(q) > 0:
        pair = q.pop(0)
        if pair in visited: continue
        visited.add(pair)
        curr, d = pair
        for back, d2 in prev[curr][d]:
            q.append((back, d2))
    count = len(set([c for c,_ in visited]))

    return newSolution(minPath, count)

if __name__ == '__main__':
    do(solve, 24, 16)

'''
Solve:
- Use modified Dijkstra's algorithm to find the shortest path from start to goal 
- Instead of just storing the shortest path to a coord, we also consider the direction from which it came from:
  this is because different shortest paths could be formed passing through different directions
- For the next states, we try to turn left/right and move forward, with cost 1001 (1000 for turn, 1 for step forward)
- We also try to move forward in the current direction, with cost 1 
- Skip next states that will hit a wall # 
- Check if we can update the shortest path of nxt coords through d2 (delta); we also consider ties so that we can update the prev backtrace
- Every time we update the shortest path of a coord, add to the list of backtrace the (coords, delta) from where we came from before we updated the value
- If the new shortest path is not a tie, we reset the list; otherwise, we keep the list and just add to it
- For Part 1, return the shortest path length from start to goal 
- For Part 2, starting from the goal, follow the backtrace (prev) to get all the unique grid cells 
  that are part of any shortest path; return the number of unique cells
- Start from the (goal, minDelta), use BFS to backtrace all the shortest paths
- When considering visited states, use the pair (coords, delta), as we might have visited this coord 
  earlier but using a different direction
'''