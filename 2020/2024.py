# Advent of Code 2020 Day 24
# John Roy Daradal 

from aoc import *

Path = tuple[str,...]
HexGrid = dict[Path, bool]

e, w, nw, ne, sw, se = 'e', 'w', 'nw', 'ne', 'sw', 'se'
hexDirections: list[str] = [ne,e,se,sw,w,nw]

OPP = {
    e   : w, 
    w   : e, 
    nw  : se, 
    se  : nw, 
    sw  : ne, 
    ne  : sw,
}

RES = {
    e   : {nw: ne, sw: se},
    w   : {ne: nw, se: sw},
    nw  : {e: ne, sw: w},
    ne  : {w: nw, se: e},
    sw  : {e: se, nw: w},
    se  : {w: sw, ne: e},
}

EXT = {
    ne  : [ne, e],
    e   : [e, se],
    se  : [se, sw],
    sw  : [sw, w],
    w   : [w, nw], 
    nw  : [nw, ne],
}

lengthPaths: dict[int, list[Path]] = {}
neighborsOf: dict[Path, list[Path]] = {}

def data(full: bool) -> list[list[str]]:
    directions: list[str] = [nw, ne, sw, se, e, w]
    def fn(line: str) -> list[str]:
        steps: list[str] = []
        while len(line) > 0:
            for d in directions: 
                if line.startswith(d):
                    steps.append(d)
                    line = line[len(d):]
                    break 
        return steps
    return [fn(line) for line in readLines(20, 24, full)]

def solve() -> Solution:
    allSteps = data(full=True)
    hexGrid: HexGrid = defaultdict(bool)

    # Part 1
    for steps in allSteps:
        path = traverseHexagon(steps)
        hexGrid[path] = not hexGrid[path]
    count1 = sum(hexGrid.values())

    # Part 2
    lengthPaths[0] = [()]
    lengthPaths[1] = [(step,) for step in hexDirections]
    for _ in range(100):
        hexGrid = nextHexGrid(hexGrid)
    count2 = sum(hexGrid.values())

    return newSolution(count1, count2)

def traverseHexagon(steps: list[str]) -> Path:
    path: list[str] = []
    for step in steps:
        path = reducePath(path, step)
    return keyOf(path)

def reducePath(path: list[str], step: str) -> list[str]:
    # Try to simplify by removing the opposite
    opp = OPP[step]
    opps = [i for i in range(len(path)) if path[i] == opp]
    if len(opps) > 0:
        idx = max(opps)
        path2 = path[:idx] + path[idx+1:]
        return path2 
    # Try to simplify by replacing with the result of combining with step
    i = len(path)-1 
    while i >= 0:
        prev = path[i]
        if step in RES[prev]:
            path2 = path[:i] + [RES[prev][step]] + path[i+1:]
            return path2
        i -= 1
    
    # Cannot simplify further, just add step to end of path
    return path + [step]

def keyOf(path: list[str]) -> Path:
    return tuple(sorted(path))

def nextHexGrid(hexGrid: HexGrid) -> HexGrid:
    maxPathLength = max(len(k) for k in hexGrid.keys()) + 1
    computeLengthPaths(maxPathLength)

    hexGrid2: HexGrid = defaultdict(bool)
    for length in range(maxPathLength+1):
        for path in lengthPaths[length]:
            keyPath = keyOf(list(path))
            nxtCount = 0
            for nxtPath in hexNeighbors(path):
                keyNext = keyOf(list(nxtPath))
                if hexGrid[keyNext]: nxtCount += 1
            hexGrid2[keyPath] = hexGrid[keyPath]
            if hexGrid[keyPath]: # black 
                if nxtCount == 0 or nxtCount > 2:
                    hexGrid2[keyPath] = False 
            else: # white
                if nxtCount == 2:
                    hexGrid2[keyPath] = True
    return hexGrid2

def computeLengthPaths(limit: int):
    for length in range(2, limit+1):
        if length in lengthPaths: continue 
        paths: list[Path] = []
        for prevPath in lengthPaths[length-1]:
            last = prevPath[-1]
            for step in EXT[last]:
                path = reducePath(list(prevPath), step)
                if len(path) != length: continue 
                paths.append(tuple(path))
        lengthPaths[length] = paths

def hexNeighbors(path: Path) -> list[Path]:
    if path == (): return lengthPaths[1]
    
    if path not in neighborsOf:
        neighbors: list[Path] = []
        for step in hexDirections:
            path2 = reducePath(list(path), step)
            neighbors.append(keyOf(path2))
        neighborsOf[path] = neighbors

    return neighborsOf[path]

if __name__ == '__main__':
    do(solve, 20, 24)

'''
Part1:
- Similar to 1711, but hexagon uses E and W instead of N and S
- OPP and RES still maps the opposite direction and the result of combining two steps
- To segment the list of steps from the whole line, check which direction matches 
  the remaining line's prefix; then remove that prefix and repeat until line is empty
- Use a defaultdict for the hexGrid so that the hexagons defaults to False (white)
- For each step list, form the path from the steps by repeatedly adding the step to the 
  path and immediately reducing the path
    - First, try to find an opposite of the added step first; if it exists, 
      the new step and its opposite cancels out, so we remove the opposite from the path 
    - If the opposite is not found, try to simplify by replacing an oldStep + newStep = resStep
      from the RES table; do this starting from the back (most recent) to the front (oldest)
    - Otherwise, the path cannot be simplified further so we just add the step to the end of the path
    - The final path is the sorted path's tuple (to make it a key in the hexGrid)
    - We sort it so that paths that refer to the same hexagon but arrive from different paths  
      will have to use the canonical form of the path (the sorted version)
- Flip the key path's entry in the hexGrid (False <=> True)
- Output the number of black (True) hexagons in the grid, after processing all steps

Part2:
- Save the paths of various lengths, as these will be the keys to the hex grid
    - For length 0, the path is () = the center of the grid 
    - For length 1, the path is the 6 hexagon directions: E, W, NW, NE, SW, SE
    - To compute the paths of length X, use the paths of length X-1
    - Then, check the last step in the path; use this to check the steps to add (EXT)
    - EXT holds the steps to add to the last step to have total coverage of all paths of that length
    - Combine the prev path and the step from EXT and reduce it; if the resulting path does not have 
      the length of interest, skip it
- Save the neighbors of each key path, to avoid recomputation:
    - For the center hexagon (), the neighbor paths are the 1-step paths (6 directions)
    - If the path is not yet in the cache, compute the neighors and save to cache
    - For each of the 6 hexagon directions, add it as a step to the current path and reduce the path
    - Add the sorted version of the new path to the neighbors list, as this is the key used in the hexagon grid
    - Return the cached nieghbors of the key path
- For 100 days, compute the next hex grid, using the current hex grid:
    - Find the maximum path length in the current hex grid
    - Ensure all length paths from 2 to maxPathLength + 1 are available
    - We add a margin 1 because a white (False) tile can become black based on its neighbors
    - Go through all entries of the hex grid so far, by checking each path length
    - For each path in the current path length, count the number of black neighbors
    - By default, the new hex grid's tile is the same as the previous, except if:
        - Current tile is black and nxtCount == 0 or nxtCount > 2 => tile becomes white (False)
        - Current tile is white and nxtCount == 2 => tile becomes black (True)
- Output the number of black (True) hexagons in the grid, after 100 days
'''