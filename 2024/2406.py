# Advent of Code 2024 Day 06
# John Roy Daradal 

from aoc import *

History = dict[coords,set[delta]]

class Config:
    def __init__(self): 
        self.bounds: dims2 = (0,0)
        self.blocked: dict[coords,bool] = defaultdict(bool)
        self.start: coords = (0,0)
        self.dir: delta = (0,0)

def data(full: bool) -> Config:
    lines = readLines(24, 6, full)
    cfg = Config()
    cfg.bounds = getBounds(lines)
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            c = (row,col)
            if char == '#':
                cfg.blocked[c] = True 
            elif char == '^':
                cfg.start = c 
                cfg.dir = U 
    return cfg

def solve() -> Solution:
    cfg = data(full=True)

    # Part 1
    visited, _ = findExit(cfg, cfg.start, cfg.dir, {})
    numVisited = len(visited)

    # Part 2
    loopPoints = countLoopPoints(cfg)

    return newSolution(numVisited, loopPoints)


def findExit(cfg: Config, start: coords, d: delta, previsit: History, obstacle: coords|None = None) -> tuple[History, bool]:
    c = start 
    visited: History = defaultdict(set)
    for k,v in previsit.items():
        visited[k] = set(v)
    visited[c].add(d)
    stuckInLoop = False
    while True:
        nxt = move(c, d)

        if not insideBounds(nxt, cfg.bounds):
            break 
        elif cfg.blocked[nxt] or nxt == obstacle:
            d = rightOf[d]
        else:
            c = nxt 
            if obstacle != None and c in visited and d in visited[c]:
                stuckInLoop = True
                break 
            visited[c].add(d)
    return visited, stuckInLoop

def countLoopPoints(cfg: Config) -> int:
    c, d = cfg.start, cfg.dir 
    obstacles = set()
    visited: History = defaultdict(set)
    visited[c].add(d)
    while True:
        nxt = move(c, d)

        if not insideBounds(nxt, cfg.bounds):
            break 
        elif cfg.blocked[nxt]:
            d = rightOf[d]
        else:
            if nxt not in visited:
                previsit = {k: set(v) for k,v in visited.items()}
                _, stuckInLoop = findExit(cfg, c, rightOf[d], previsit, nxt)
                if stuckInLoop:
                    obstacles.add(nxt)

            c = nxt 
            visited[c].add(d)

    return len(obstacles)

if __name__ == '__main__':
    do(solve, 24, 6)

'''
Part1:
- Simulate the guard movements until he finds the exit (out of bounds); output the number of steps to exit 
- Start at the ^ position; keep track of the direction each time a cell is visited (to detect loops)
- Try to move to the next position using the current delta
    - If already out of bounds, the guard has exited = done.
    - If next position is blocked #, we turn the delta to the right 
    - Otherwise, we move to the next position; update visited of the previous position with the current delta
    - If point has already been visited and in the same direction, you are stuck in a loop = exit

Part2:
- Count the number of points in the grid where if you put an obstacle will cause the guard to loop 
- Move the guard similar to Part 1 (if exit = done, if blocked = turn right)
- For the next position, simulate what would happen if we put an obstacle in that position
    - Run the findExit function from Part 1, with a temporary obstacle on the next position
    - Also pass in the points already visited with their deltas (for loop detection)
    - If the simulation results in a loop, add the next position to list of points for obstacles
- Output the number of possible obstacles that will cause the loop
'''