# Advent of Code 2024 Day 20
# John Roy Daradal 

from aoc import *

Grid = list[str]
Cheat = tuple[coords, coords] # (start, end)
CheatStep = tuple[Cheat, int] # (cheat, steps)

def data(full: bool) -> tuple[Grid, coords]:
    grid = readLines(24, 20, full)
    rows,cols = getBounds(grid)
    start = [(r,c) for r in range(rows) for c in range(cols) if grid[r][c] == 'S'][0]
    return grid, start

def solve() -> Solution:
    grid, start = data(full=True)
    sp = bfsShortestPath(grid, start)

    # Part 1 
    count1 = countTotalCheats(grid, sp, 2)

    # Part 2
    count2 = countTotalCheats(grid, sp, 20)

    return newSolution(count1, count2)

def countTotalCheats(grid: Grid, sp: dict[coords, int], cheatLimit: int) -> int:
    cheats: dict[int, set[Cheat]] = defaultdict(set)
    path = sorted([(dist, pt) for pt,dist in sp.items()])
    for dist, pt in path:
        for (cheatStart, cheatEnd), cheatSteps in findCheats(grid, pt, cheatLimit):
            # make sure we are moving forward 
            if sp[cheatEnd] <= dist: continue 
            # make sure we are saving time
            timeSave = sp[cheatEnd] - dist - cheatSteps 
            if timeSave <= 0: continue
            cheats[timeSave].add((cheatStart, cheatEnd))

    count = 0
    for timeSave, cheatPairs in cheats.items():
        if timeSave < 100: continue 
        count += len(cheatPairs)

    return count

def bfsShortestPath(grid: Grid, start: coords) -> dict[coords, int]:
    q: list[tuple[coords, int]] = [(start, 0)]
    sp: dict[coords, int] = {}
    while len(q) > 0:
        curr, steps = q.pop(0)
        if curr in sp: continue 
        sp[curr] = steps 
        for nxt in surround4(curr):
            ny,nx = nxt 
            if nxt in sp or grid[ny][nx] == '#': continue 
            q.append((nxt, steps+1))
    return sp

def findCheats(grid: Grid, start: coords, limit: int) -> list[CheatStep]:
    bounds = getBounds(grid)
    q: list[CheatStep] = []
    for nxt in surround4(start):
        q.append(((nxt, nxt), 1))

    visited: set[coords] = set()
    visited.add(start)

    candidates: set[CheatStep] = set()
    while len(q) > 0:
        cheat, steps = q.pop(0)
        cheatStart, curr = cheat
        if curr in visited: continue 
        visited.add(curr)
        candidates.add((cheat, steps))
        if steps == limit: continue 
        for nxt in surround4(curr):
            if nxt in visited or not insideBounds(nxt, bounds): continue 
            q.append(((cheatStart, nxt), steps+1))

    cheats: list[CheatStep] = []
    for cheat, steps in candidates:
        y,x = cheat[1] # cheatEnd 
        if grid[y][x] != '#':
            cheats.append((cheat, steps))
    return cheats

if __name__ == '__main__':
    do(solve, 24, 20)

'''
Solve: 
- Use BFS to traverse from the start to the goal (only 1 path): return a dictionary  
  mapping the coords in the path to the distance from start (step count)
- Process the path starting from start to goal (sorted in increasing step count)
- From the current position, find possible cheats within the given cheatLimit:
    - Use BFS to explore parts of the grid reachable within the cheatLimit
    - Since we are in cheat mode, we can ignore walls, as long as we don't go out of bounds
    - Initialize the queue with the 4 surrounding cells of the current position (UDLR), with step=1
    - Mark start position as visited already, since we dont want to come back to it (and it wont be added to the queue)
    - The BFS states are in the form: (cheatStart, currentPosition), numSteps 
    - While exploring, add any reachable state with number of steps as candidates
    - We stop exploring the current node if the numSteps has reached the cheatLimit 
    - Otherwise, we check the 4 neighbors (UDLR) and add them to the queue
    - From the list of candidates, filter out those that end in '#' (have to be in a free track after cheat ends)
- From the found cheats, skip those that will make us go backward or will not save time
- Group the valid cheats by the time they will save us
- Time saved by using the cheat is sp[cheatEnd] - sp[curr] - cheatSteps:
    - The time saved by using the cheat is the difference between where we end up in (sp[cheatEnd]) 
      and our step count from the current position
    - But since we are using cheatSteps to achieve this, we also subtract that value (cost)
- From the grouped cheats by time saved, filter out those that will not save at least 100
- Get the total number of cheats from the valid time saved (>= 100)
- For Part 1, count total cheats with cheatLimit = 2
- For Part 2, count total cheats with cheatLimit = 20
'''