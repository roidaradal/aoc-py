# Advent of Code 2020 Day 17
# John Roy Daradal 

from aoc import *

Cube = dict[int3, bool]
Quad = dict[int4, bool]

def data(full: bool) -> list[tuple[coords,bool]]:
    points: list[tuple[coords,bool]] = []
    grid = readLines(20, 17, full)
    for y,line in enumerate(grid):
        for x,char in enumerate(line):
            points.append(((y,x), char == '#'))
    return points

def solve() -> Solution:
    points = data(full=True)

    # Part 1
    cube: Cube = defaultdict(bool)
    for (y,x),active in points:
        cube[(0,y,x)] = active

    for _ in range(6):
        cube = nextCube(cube)
    active1 = sum(cube.values())

    # Part 2
    quad: Quad = defaultdict(bool)
    for (y,x),active in points:
        quad[(0,0,y,x)] = active 

    for _ in range(6):
        quad = nextQuad(quad)
    active2 = sum(quad.values())

    return newSolution(active1, active2)

def nextCube(cube: Cube) -> Cube:
    cube2: Cube = defaultdict(bool)
    zs = set(t[0] for t, active in cube.items() if active)
    ys = set(t[1] for t, active in cube.items() if active)
    xs = set(t[2] for t, active in cube.items() if active)
    minZ, maxZ = min(zs)-1, max(zs)+2 # +1 for margin, +1 for limit
    minY, maxY = min(ys)-1, max(ys)+2 
    minX, maxX = min(xs)-1, max(xs)+2
    for z in range(minZ, maxZ):
        for y in range(minY, maxY):
            for x in range(minX, maxX):
                cube2[(z,y,x)] = nextCubeState(cube, (z,y,x))
    return cube2

def nextCubeState(cube: Cube, t: int3) -> bool:
    isActive = cube[t]
    activeNeighbors = sum(cube[n] for n in neighborCubes(t))
    if isActive:
        return activeNeighbors in (2,3)
    else:
        return activeNeighbors == 3

def neighborCubes(t: int3) -> list[int3]:
    z, y, x = t
    neighbors: list[int3] = []
    for ny,nx in surround8((y,x)):
        for zd in (-1,0,1):
            neighbors.append((z+zd, ny, nx))
    neighbors.append((z-1, y, x))
    neighbors.append((z+1, y, x))
    return neighbors

def nextQuad(quad: Quad) -> Quad:
    quad2: Quad = defaultdict(bool)
    ws = set(q[0] for q, active in quad.items() if active)
    zs = set(q[1] for q, active in quad.items() if active)
    ys = set(q[2] for q, active in quad.items() if active)
    xs = set(q[3] for q, active in quad.items() if active)
    minW, maxW = min(ws)-1, max(ws)+2 # +1 for margin, +1 for limit
    minZ, maxZ = min(zs)-1, max(zs)+2 
    minY, maxY = min(ys)-1, max(ys)+2 
    minX, maxX = min(xs)-1, max(xs)+2
    for w in range(minW, maxW):
        for z in range(minZ, maxZ):
            for y in range(minY, maxY):
                for x in range(minX, maxX):
                    quad2[(w,z,y,x)] = nextQuadState(quad, (w,z,y,x)) 
    return quad2

def nextQuadState(quad: Quad, q: int4) -> bool:
    isActive = quad[q]
    activeNeighbors = sum(quad[n] for n in neighborQuads(q))
    if isActive:
        return activeNeighbors in (2,3)
    else:
        return activeNeighbors == 3 
    
def neighborQuads(q: int4) -> list[int4]:
    w, z, y, x = q 
    neighbors: list[int4] = []
    diffs = (-1,0,1)
    for wd in diffs:
        for zd in diffs:
            for yd in diffs:
                for xd in diffs: 
                    if (wd, zd, yd, xd) == (0,0,0,0): continue 
                    neighbors.append((w+wd, z+zd, y+yd, x+xd))
    return neighbors

if __name__ == '__main__':
    do(solve, 20, 17)

'''
Part1:
- Convert the 2D grid input into 3D space by copying the y,x into z=0 
- For 6 cycles, compute the next cube:
    - Extract the current x, y, z values from the active items in the cube 
    - Choose the min and max for each dimension
    - Extend your search by starting from min-1 and upto max+1
    - Reason: since this is the last layer that has active items, it can affect the 
      computation of the previous/next layer at that dimension
    - Compute the next cube state by checking the active count among the 26 neighbors
    - To compute the neighbors: get surround8 for y,x then repeat it for same z, z-1, and z+1
    - Also add the z-1 and z+1 versions of the current coords
- Output the number of active items after 6 cycles

Part2:
- Convert the 2D grid input into 4D space by copying the y,x into w=0, z=0
- For 6 cycles, compute the next quad:
    - Extract the current w, x, y, z values from the active items in the quad 
    - Choose the min  max for each dimension and extend search by -1 and +1 (similar to Part 1)
    - Compute the next quad state by checking the active count among the 80 neighbors
    - To compute the neighbors: get the d-1, d, d+1 for all dimensions, skip the tuple where all diffs are 0
- Output the number of active items after 6 cycles 
'''