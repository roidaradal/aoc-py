# Advent of Code 2018 Day 22
# John Roy Daradal 

import heapq
from aoc import *

# minutes, tool, position
State = tuple[int, int, coords]

ROCKY, WET, NARROW = 0, 1, 2
NONE, CLIMB, TORCH = 0, 1, 2 
STEP_COST   = 1 
SWITCH_COST = 7

allowedTools: dict[int, list[int]] = {
    ROCKY   : [CLIMB, TORCH],
    WET     : [NONE, CLIMB],
    NARROW  : [NONE, TORCH],
}

depth:  int = 0 
target: coords = (0,0)
erosion: dict[coords, int] = {}

def data(full: bool) -> tuple[int, coords]:
    line1, line2 = readLines(18, 22, full)
    depth = int(splitStr(line1, ':')[1])
    x,y = toInt2(splitStr(line2, ':')[1], ',')
    return depth, (y,x)

def solve() -> Solution:
    global depth, target
    depth, target = data(full=True)

    # Part 1
    ymax, xmax = target
    for y in range(ymax+1):
        for x in range(xmax+1):
            getErosionLevel((y,x))
    risk = sum(x % 3 for x in erosion.values())

    # Part 2
    sp: dict[coords, dict[int, int]] = defaultdict(lambda: defaultdict(lambda: sys.maxsize))
    pq: list[State] = []
    heapq.heappush(pq, (0, TORCH, (0,0)))

    while len(pq) > 0:
        cost, tool, curr = heapq.heappop(pq)
        currTerrain = getTerrainType(curr)

        nxtStates: list[State] = []
        for nxt in surround4(curr):
            ny, nx = nxt 
            if ny < 0 or nx < 0: continue # skip negative coords 

            nxtTerrain = getTerrainType(nxt)
            cost2 = cost + STEP_COST
            if tool in allowedTools[nxtTerrain]:
                # continue using same tool on next cell
                nxtStates.append((cost2, tool, nxt))
            else:
                # switch to allowed tools, add switch cost
                # allow switch if current terrain also allows the tool
                cost2 += SWITCH_COST
                for tool2 in allowedTools[nxtTerrain]:
                    if tool2 not in allowedTools[currTerrain]: continue
                    nxtStates.append((cost2, tool2, nxt))

        bestTargetCost = getBestTargetCost(sp)
        for nxtState in nxtStates:
            cost2, tool2, nxt = nxtState
            if cost2 > bestTargetCost: continue # skip if cannot be better than current maxTargetCost
            if sp[nxt][tool2] > cost2:
                sp[nxt][tool2] = cost2 
                heapq.heappush(pq, nxtState)

    torchCost = sp[target][TORCH]
    climbCost = sp[target][CLIMB] + SWITCH_COST # have to switch to torch
    minCost = min(torchCost, climbCost)

    return newSolution(risk, minCost)

def getErosionLevel(pt: coords) -> int: 
    if pt not in erosion:
        y,x = pt
        geo = 0 
        if pt == (0,0) or pt == target:
            geo = 0
        elif y == 0:
            geo = x * 16807 
        elif x == 0:
            geo = y * 48271
        else:
            left = getErosionLevel((y,x-1))
            top  = getErosionLevel((y-1,x))
            geo = left * top 
        erosion[pt] = (geo + depth) % 20183
    return erosion[pt]

def getTerrainType(pt: coords) -> int:
    return getErosionLevel(pt) % 3

def getBestTargetCost(sp: dict[coords, dict[int,int]]) -> int:
    choices: list[int] = [sys.maxsize]
    for tool, cost in sp[target].items():
        if tool != TORCH: cost += SWITCH_COST 
        choices.append(cost)
    return min(choices)

if __name__ == '__main__':
    do(solve, 18, 22)

'''
Part1:
- From (0,0) to the target position, compute the erosion level:
    - At (0,0) and the target position, the geologic index is 0 
    - If y == 0, geo index is x * 16807
    - If x == 0, geo index is y * 48271
    - Otherwise, geo index = erosion[(y,x-1)] * erosion[(y-1,x)] (left * top)
    - Erosion level at position = (geo + depth) % 20183
- The terrain type of each position is erosionLevel % 3: 0=ROCKY, 1=WET, 2=NARROW
- Total risk level is the sum of terrain types from (0,0) to target position 

Part2:
- Use modified Dijkstra's to find the shortest path from (0,0) to the target position, while considering
  the current tool being held at each position
- Start at (0,0) holding the torch
- The priority queue's key is the current path cost
- At the current position, consider the 4 neighbors that will not give negative coordinates
- The cost of going from current position to the next is the STEP_COST=1
- If the tool we are currently holding is also allowed by the next position's terrain, we continue using the
  same tool on the next cell (next cost is only the step cost)
- Otherwise, we need to switch to the allowed tools, but only if the current terrain also allows the tool 
- Add the cost of switching from current tool to a new one (or none): SWITCH_COST=7
- Get the current best cost at the target: min(sp[target][TORCH], sp[target][CLIMB]+SWITCH_COST)
- If the next state's cost cannot be better than the current best, we skip it (prune)
- If the next state's cost will be better than sp[nxt][tool2], update the shortest path value and add to PQ
- After processing all items in the PQ, get the min cost at the target position:
  min(sp[target][TORCH], sp[target][CLIMB] + SWITCH_COST), need to switch to torch if we are using climbing gear
'''