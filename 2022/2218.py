# Advent of Code 2022 Day 18
# John Roy Daradal 

import itertools
from aoc import *

Grid = dict[int3, bool]
Bounds3 = tuple[dims3, dims3]
Graph = dict[int3, list[int3]]

TOP, BOT = 0, 1 
LEFT, RIGHT = 2, 3
FRONT, BACK = 4, 5

OPP = { 
    TOP: BOT, BOT: TOP, 
    LEFT: RIGHT, RIGHT: LEFT, 
    FRONT: BACK, BACK: FRONT
}

deltas: dict[int, int3] = {
    TOP     : (0, -1, 0),
    BOT     : (0, 1, 0),   
    LEFT    : (-1, 0, 0), 
    RIGHT   : (1, 0, 0),  
    FRONT   : (0, 0, -1),
    BACK    : (0, 0, 1),
}

class Cube:
    def __init__(self, pos: int3):
        self.pos = pos 
        self.visible = {face: True for face in [TOP, BOT, LEFT, RIGHT, FRONT, BACK]}
    
    def __repr__(self) -> str:
        x,y,z = self.pos
        return '(%d,%d,%d)' % (x,y,z)
    
    def checkCoveredSides(self, grid: Grid):
        for face, d in deltas.items():
            nxt = move3(self.pos, d)
            if grid[nxt]:
                self.visible[face] = False 
    
    def countVisible(self) -> int:
        return sum(1 for face in self.visible if self.visible[face])

def data(full: bool) -> list[Cube]:
    def fn(line: str) -> Cube:
        pos = toInt3(line, ',')
        return Cube(pos)
    return [fn(line) for line in readLines(22, 18, full)]

def solve() -> Solution:
    cubes = data(full=True)
    grid: Grid = defaultdict(bool)

    # Part 1
    for cube in cubes:
        grid[cube.pos] = True 
    for cube in cubes:
        cube.checkCoveredSides(grid)
    total1 = getTotal(cubes, Cube.countVisible)

    # Part 2
    bounds = getCubeBounds(grid)
    gaps = findGaps(grid, bounds)
    graph = createGapGraph(gaps)
    faceGaps = getFaceGaps(gaps, bounds)

    allReachable: set[int3] = set()
    for faceGap in faceGaps:
        if faceGap in allReachable: continue
        reachable = floodFillCube(graph, faceGap)
        allReachable = allReachable.union(reachable)

    internal: dict[int3, set[int]] = defaultdict(set)
    for gap in gaps:
        if gap in allReachable: continue
        blocks = findBlockers(grid, bounds, gap)
        if len(blocks) != 6: continue 
        for pos, face in blocks.items():
            internal[pos].add(face)

    for cube in cubes:
        if cube.pos not in internal: continue 
        for face in internal[cube.pos]:
            cube.visible[face] = False
    total2 = getTotal(cubes, Cube.countVisible)

    return newSolution(total1, total2)

def move3(pos: int3, d: int3) -> int3:
    x,y,z = pos 
    dx,dy,dz = d 
    return (x+dx, y+dy, z+dz)

def getCubeBounds(grid: Grid) -> Bounds3:
    inf = sys.maxsize 
    xmin, ymin, zmin = inf, inf, inf 
    xmax, ymax, zmax = 0, 0, 0
    for pos, hasCube in grid.items():
        if not hasCube: continue
        x, y, z = pos
        xmin, ymin, zmin = min(xmin, x), min(ymin, y), min(zmin, z) 
        xmax, ymax, zmax = max(xmax, x), max(ymax, y), max(zmax, z)
    return ((xmin, ymin, zmin), (xmax+1, ymax+1, zmax+1))

def findGaps(grid: Grid, bounds: Bounds3) -> list[int3]:
    (xstart, ystart, zstart), (xend, yend, zend) = bounds
    gaps: list[int3] = []
    for x in range(xstart, xend):
        for y in range(ystart, yend):
            for z in range(zstart, zend):
                if not grid[(x,y,z)]:
                    gaps.append((x,y,z))
    return gaps

def findBlockers(grid: Grid, bounds: Bounds3, pos: int3) -> dict[int3, int]:
    (xstart, ystart, zstart), (xend, yend, zend) = bounds
    blockers: dict[int3, int] = {}
    shouldStop = {
        FRONT   : lambda t: t[2] < zstart, 
        BACK    : lambda t: t[2] >= zend,
        TOP     : lambda t: t[1] < ystart, 
        BOT     : lambda t: t[1] >= yend,
        LEFT    : lambda t: t[0] < xstart, 
        RIGHT   : lambda t: t[0] >= xend,
    }
    for face, d in deltas.items():
        curr = pos 
        while not shouldStop[face](curr):
            curr = move3(curr, d)
            if grid[curr]:
                blockers[curr] = OPP[face]
                break
    return blockers

def getFaceGaps(gaps: list[int3], bounds: Bounds3) -> list[int3]:
    faceGaps: list[int3] = []
    (xstart, ystart, zstart), (xend, yend, zend) = bounds
    for gap in gaps:
        x,y,z = gap 
        if x == xstart or x == xend-1:
            faceGaps.append(gap)
        elif y == ystart or y == yend-1:
            faceGaps.append(gap)
        elif z == zstart or z == zend-1:
            faceGaps.append(gap)
    return faceGaps

def isAdjacent(t1: int3, t2: int3) -> bool:
    return sum(abs(t1[i]-t2[i]) for i in range(3)) == 1

def createGapGraph(gaps: list[int3]) -> Graph:
    graph: Graph = defaultdict(list)
    for t1, t2 in itertools.combinations(gaps, 2):
        if not isAdjacent(t1, t2): continue 
        graph[t1].append(t2)
        graph[t2].append(t1)
    return graph

def floodFillCube(graph: Graph, start: int3) -> set[int3]:
    visited: set[int3] = set()
    q: list[int3] = [start]
    while len(q) > 0:
        t = q.pop(0)
        if t in visited: continue 
        visited.add(t)
        for nxt in graph[t]:
            if nxt in visited: continue 
            q.append(nxt)
    return visited

if __name__ == '__main__':
    do(solve, 22, 18)

'''
Part1:
- Build the 3D cube grid by putting the positions of the cube inputs in the grid
- For each cube, check each face if it is covered, using the built grid 
- For each of the 6 faces, try to see if there is a cube in that direction in the grid
- If there is a neighbor cube in that direction, we set visible[face] = False
- For each cube, count the total number of visible faces
- Return the total number of visible faces for all cubes

Part2:
- Get the cube bounds by getting the min/max x,y,z values from the grid 
- Find the gaps in the cube - candidate air pockets:
- Go through the x, y, and z ranges and if there is not a cube in (x,y,z), it is a gap
- Create the gap graph by checking if two gaps are connected: go through all possible pair 
  combinations of gaps, and if they are adjacent, add an edge between them
- Two gaps are considered adjacent if they differ by 1 in exactly 1 axis:
    - Example: (2,2,3) and (2,2,4), (2,1,3) and (2,0,3)
    - Anti-Example: (2,2,3) and (2,3,4) - they differ by 1 in two axes
- Get the gaps that are on the external or face side of the grid cube:
- It is a face gap if the gap's x, y, or z coordinate is either the start or the end of that axis' range
- The face gaps are where we will start to do our flood fill, since these are the most external gaps there are
- Starting at each face gap, except for the ones already visited in another round, check all the reachable gaps 
  by doing a 3D flood-fill; this will identify all gaps reachable from outside = these are not air pockets
- To do the 3D flood-fill, it is basically a BFS using the gap grap created above
- Keep track of all the reachable gaps from the flood fills, so we can rule them out as air pockets later
- For each of the unreachable gaps (these are our candidate air pockets):
    - Find its blockers in the 6 directions 
    - If it doesn't have 6 blockers, it's not a valid air pocket as it's not trapped in all sides 
    - For the valid air pockets, set the blocker's face in the opposite direction to be not visible 
- To find a blocker in one direction, repeatedly move in that direction until we either find a blocker (a cube in the grid),
  or we reach the end of the cube grid bounds (stop = there is no blocker in this direction)
- Repeat this process for each of the 6 directions; a valid air pocket will have 6 valid blockers = it's trapped inside the cube
- We make the blocker's face in the opposite direction not visible:
    - Example: if we are finding a blocker on top, it is the blocker's bottom that should not be visible
- Return the total number of visible faces for all cubes
'''