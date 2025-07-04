# Advent of Code 2019 Day 18
# John Roy Daradal 

from functools import cache
from aoc import *

Grid = tuple[str,...]
Quad = tuple[coords,coords,coords,coords]
Goal = tuple[int,str,int]
Items = dict[str, coords]
Info = tuple[Items, Items] # keys, doors
info: Info = ({},{})

def data(full: bool) -> Grid:
    return tuple(readLines(19,18, full))

def solve() -> Solution:
    global info
    grid = data(full=True)
    curr, info = findItems(grid)
    
    # Part 1 
    sp1 = findShortestPath(grid, curr)

    # Part 2 
    quad, grid = adjustGrid(grid, curr)
    sp2 = findShortestTotal(grid, quad)

    return newSolution(sp1, sp2)

def adjustGrid(grid: Grid, curr: coords) -> tuple[Quad, Grid]:
    grid2 = [list(line) for line in grid]
    y, x = curr 
    line1 = grid2[y-1]
    line2 = grid2[y]
    line3 = grid2[y+1]
    grid2[y-1] = line1[:x-1] + list('@#@') + line1[x+2:]
    grid2[y]   = line2[:x-1] + list('###') + line2[x+2:]
    grid2[y+1] = line3[:x-1] + list('@#@') + line3[x+2:]
    grid = tuple(''.join(line) for line in grid2)
    quad: Quad = ((y-1,x-1),(y-1,x+1),(y+1,x-1),(y+1,x+1))
    return quad, grid

def findItems(grid: Grid) -> tuple[coords, Info]:
    keys: Items = {}
    doors: Items = {}
    curr: coords = (0,0)
    for row,line in enumerate(grid):
        for col,char in enumerate(line):
            if char in '.#': continue
            if char == '@':
                curr = (row,col)
            elif char.islower():
                keys[char] = (row,col)
            elif char.isupper():
                doors[char.lower()] = (row,col)
    return curr, (keys, doors)

def findReachableKeys(grid: Grid, curr: coords) -> list[strInt]:
    reachable: list[strInt] = []
    visited: set[coords] = set()
    q: list[tuple[coords,int]] = [(curr, 0)]
    while len(q) > 0:
        curr, steps = q.pop(0)
        if curr in visited: continue 
        visited.add(curr)
        for nxt in surround4(curr):
            ny,nx = nxt 
            nxtTile = grid[ny][nx]
            if nxtTile == '.' and nxtTile not in visited:
                q.append((nxt, steps+1))
            elif isKey(nxtTile):
                reachable.append((nxtTile, steps+1))
    return reachable

def findQuadReachableKeys(grid: Grid, quad: Quad) -> list[Goal]:
    reachable: list[Goal] = []
    visited: set[coords] = set()
    q: list[tuple[int, coords, int]] = [
        (0, quad[0], 0),
        (1, quad[1], 0), 
        (2, quad[2], 0),
        (3, quad[3], 0),
    ]
    while len(q) > 0:
        idx, curr, steps = q.pop(0)
        if curr in visited: continue 
        visited.add(curr)
        for nxt in surround4(curr):
            ny,nx = nxt 
            nxtTile = grid[ny][nx]
            if nxtTile == '.' and nxtTile not in visited:
                q.append((idx, nxt, steps+1))
            elif isKey(nxtTile):
                reachable.append((idx, nxtTile, steps+1))
    return reachable

def isKey(tile: str) -> bool:
    return tile not in '#.@' and tile.islower()

def isDoor(tile: str) -> bool:
    return tile not in '#.@' and tile.isupper()

def gotoKey(grid: Grid, curr: coords, keyPos: coords) -> tuple[Grid, coords]:
    grid2 = [list(line) for line in grid]
    y,x = curr 
    grid2[y][x] = '.'
    ky,kx = keyPos 
    grid2[ky][kx] = '@'
    grid = tuple(''.join(line) for line in grid2)
    return grid, keyPos

def openDoor(grid: Grid, door: coords) -> Grid:
    grid2 = [list(line) for line in grid]
    y,x = door 
    grid2[y][x] = '.'
    return tuple(''.join(line) for line in grid2)

def nextGrid(grid: Grid, curr: coords, key: str) -> tuple[coords, Grid]:
    keys, doors = info
    # Go to chosen key 
    grid2, curr = gotoKey(grid, curr, keys[key])
    # Open door if applicable 
    if key in doors: 
        grid2 = openDoor(grid2, doors[key])
    return curr, grid2

def nextQuadGrid(grid: Grid, quad: Quad, idx: int, key: str) -> tuple[Quad, Grid]:
    keys, doors = info 
    quad2 = list(quad)
    # Go to chosen key 
    grid2, quad2[idx] = gotoKey(grid, quad[idx], keys[key])
    a,b,c,d = quad2
    # Open door if applicable 
    if key in doors:
        grid2 = openDoor(grid2, doors[key])
    return (a,b,c,d), grid2

@cache
def findShortestPath(grid: Grid, curr: coords) -> int:
    totalSteps = 0 
    while True:
        reachable = findReachableKeys(grid, curr)
        if len(reachable) == 0: break # no more keys 

        if len(reachable) > 1: 
            minSteps: int = sys.maxsize
            for key, steps in reachable:
                curr2, grid2 = nextGrid(grid, curr, key)
                sp = findShortestPath(grid2, curr2)
                sp += steps 
                minSteps = min(minSteps, sp)
            return totalSteps + minSteps
        else:
            key, steps = reachable[0]
            curr, grid = nextGrid(grid, curr, key)
            totalSteps += steps

    return totalSteps

@cache 
def findShortestTotal(grid: Grid, quad: Quad) -> int: 
    totalSteps = 0
    while True:
        reachable = findQuadReachableKeys(grid, quad)
        if len(reachable) == 0: break # no more reachable

        if len(reachable) > 1:
            minSteps: int = sys.maxsize 
            for idx, key, steps in reachable:
                quad2, grid2 = nextQuadGrid(grid, quad, idx, key)
                sp = findShortestTotal(grid2, quad2)
                sp += steps 
                minSteps = min(minSteps, sp)
            return totalSteps + minSteps
        else:
            idx, key, steps = reachable[0]
            quad, grid = nextQuadGrid(grid, quad, idx, key)
            totalSteps += steps
    return totalSteps


if __name__ == '__main__':
    do(solve, 19, 18)

'''
Part1:
- Scan the grid to find the keys, doors, and current position
- Find the shortest path to collect all the keys in the grid
- Repeat until no more keys in the grid:
    - Use BFS to find the reachable keys from the current position
    - Return list of reachable (keys, number of steps to get there)
    - If only 1 reachable key, move to the key's position and open the 
      corresponding door, if any; increment the totalSteps by the key steps
    - If multiple reachable keys, compute the next grid state and position if 
      we choose tho visit this key; then recursively call findShortestPath on it
    - Try this for all key options, and choose the one with minimum steps
    - Return current totalSteps + minSteps of the chosen branch
- Use functools.cache to memoize the repeated grid/curr states

Part2:
- Transform the grid by converting 1 robot into 4, and dividing the grid into 4 quadrants
- Find the shortest total path for the 4 robots to collect all keys
- Similar to Part 1, but the steps are adjusted to use 4 robot coordinates instead of 1
- In findQuadReachableKeys, we get all the reachable keys from the 4 robots and indicate the
  robot index of who will move to reach the key
- In nextQuadGrid, we update the position of the chosen robot index
'''