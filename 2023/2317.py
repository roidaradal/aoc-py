# Advent of Code 2023 Day 17
# John Roy Daradal 

import heapq
from aoc import *

Step = tuple[delta, int]

def data(full: bool) -> IntGrid:
    return [toIntLine(line) for line in readLines(23, 17, full)]

def solve() -> Solution:
    grid = data(full=True)

    # Part 1 
    loss1 = minHeatLoss(grid, (0,3))

    # Part 2 
    loss2 = minHeatLoss(grid, (4, 10))

    return newSolution(loss1, loss2)

def minHeatLoss(grid: IntGrid, turnLimits: int2) -> int:
    minStraight, maxStraight = turnLimits 

    bounds = getBounds(grid)
    rows, cols = bounds 
    sp: dict[coords, dict[Step, int]] = {}
    for r in range(rows):
        for c in range(cols):
            sp[(r,c)] = defaultdict(lambda: sys.maxsize)

    start: coords = (0, 0)
    pq: list[tuple[int, coords, delta, int]] = []
    heapq.heappush(pq, (0, start, R, 0))
    heapq.heappush(pq, (0, start, D, 0))
    while len(pq) > 0:
        total, curr, d, count = heapq.heappop(pq)
        nxtStates: list[tuple[coords, delta, int]]= []

        # Turn Left / Right, if count >= minStraight
        if count >= minStraight:
            for turn in [leftOf, rightOf]:
                d2 = turn[d]
                nxt = move(curr, d2)
                nxtStates.append((nxt, d2, 1))

        # Continue in current direction if count < maxStraight 
        if count < maxStraight:
            nxt = move(curr, d)
            nxtStates.append((nxt, d, count+1))
        
        for nxt, d2, count2 in nxtStates:
            if not insideBounds(nxt, bounds): continue
            ny,nx = nxt 
            cost = grid[ny][nx]
            step: Step = (d2, count2)
            if sp[nxt][step] > total + cost:
                sp[nxt][step] = total + cost
                heapq.heappush(pq, (sp[nxt][step], nxt, d2, count2))

    goal = (rows-1,cols-1)
    return min(sp[goal].values())

if __name__ == '__main__':
    do(solve, 23, 17)

'''
Solve: 
- For Part 1, solve for min heat loss, with minStraight = 0, maxStraight = 3
- For Part 2, solve for min heat loss, with minStaright = 4, maxStraight = 10
- Use a modified Dijkstra's algorithm to find the min heat loss from (0,0) to the bottom-right corner
- For each grid cell, we keep track of the shortest path, considering the step taken to get there:
    - Instead of a dict[coords,int] for the cells, we use a dict[coords, dict[Step,int]]
    - A step is a tuple of (delta, int), which tells us the current direction and number of steps taken so far in that direction
    - We break down the shortest path for each cell into the steps that brought them there
    - Use a defaultdict that gives sys.maxsize (inf) shortest path values for the grid cells and any step
- Use a heap PQ to implement Dijkstra's: the priority is the total heatLoss so far, and we add the 
  current position, current direction, and number of steps in that direction for the state
- To process the next state of a popped state from the heap PQ, we consider turning left/right or going straight:
    - If the number of steps in the current direction >= minStraight, we can turn left/right
    - The next state will go to the next coordinate, using the new direction, and resetting the stepCount to 1
    - If the number of steps in the current direction < maxStraight, we can continue going forward in the current direction
    - The next state will go to the next coordinate, using the same direction, and incrementing the stepCount
- For each of the next states, skip if the next coords go out of bounds
- The cost of entering the next coord is the number value in the grid
- The step key to access the shortest path dictionary is (nxtDirection, nxtStepCount)
- If we can improve the shortest path of the next coords with the step key, by instead using
  totalHeatLoss + cost of entering next cell, we update it and add the next state to the heap PQ 
- Check the values in the goal cell, and return the minimum heatLoss in that cell
'''