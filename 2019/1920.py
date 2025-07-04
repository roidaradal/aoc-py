# Advent of Code 2019 Day 20
# John Roy Daradal 

from aoc import *

Grid = list[str]
Position = tuple[coords,int] # coords, level

def data(full: bool) -> Grid:
    return [line.strip('\n') for line in readLines(19, 20, full, strip=False)]

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    grid = data(full=True)
    aa, zz, portals = analyzeGrid(grid)
    q: list[tuple[coords,int]] = [(aa, 0)]
    visited: set[coords] = set()
    while True:
        curr, steps = q.pop(0)
        if curr in visited: continue 
        visited.add(curr)
        if curr == zz: return steps 
        
        nextCoords = surround4(curr)
        if curr in portals:
            nextCoords.append(portals[curr])
        for nxt in nextCoords:
            ny,nx = nxt 
            if grid[ny][nx] == '.' and nxt not in visited:
                q.append((nxt, steps+1))

def part2() -> int:
    grid = data(full=True)
    aa, zz, portals = analyzeGrid2(grid)
    q: list[tuple[Position, int]] = [((aa, 0), 0)]
    visited: set[Position] = set()
    while True:
        position, steps = q.pop(0)
        if position in visited: continue 
        visited.add(position)
        if position == (zz, 0): return steps
        
        curr, level = position 
        nextPositions = [(c, level) for c in surround4(curr)]
        if curr in portals:
            nxt, levelAdjust = portals[curr]
            isWall = level == 0 and levelAdjust == -1
            if not isWall:
                nextPositions.append((nxt, level+levelAdjust))
        for nxtPos in nextPositions:
            ny, nx = nxtPos[0] 
            if grid[ny][nx] == '.' and nxtPos not in visited:
                q.append((nxtPos, steps+1))

def isLetter(tile: str) -> bool:
    return 65 <= ord(tile) <= 90 # A-Z

def analyzeGrid(grid: Grid) -> tuple[coords,coords,dict[coords,coords]]:
    rows, cols = getBounds(grid)
    aa: coords = (0,0)
    zz: coords = (0,0)
    pairs: dict[str,list[coords]] = defaultdict(list)
    for row in range(1, rows-1):
        for col in range(1, cols-1):
            char = grid[row][col]
            if char != '.': continue 
            (uy,ux),(ly,lx),(ry,rx),(dy,dx) = surround4((row,col))
            name = ''
            if isLetter(grid[uy][ux]):
                name = grid[uy-1][ux] + grid[uy][ux]
            elif isLetter(grid[dy][dx]):
                name = grid[dy][dx] + grid[dy+1][dx]
            elif isLetter(grid[ly][lx]):
                name = grid[ly][lx-1] + grid[ly][lx]
            elif isLetter(grid[ry][rx]):
                name = grid[ry][rx] + grid[ry][rx+1]
            
            if name == '': 
                continue 
            elif name == 'AA':
                aa = (row,col)
            elif name == 'ZZ':
                zz = (row,col)
            else:
                pairs[name].append((row,col))

    portals: dict[coords,coords] = {}
    for group in pairs.values():
        p1, p2 = group 
        portals[p1] = p2 
        portals[p2] = p1

    return aa, zz, portals

def analyzeGrid2(grid: Grid) -> tuple[coords, coords, dict[coords, Position]]:
    bounds = getBounds(grid)
    rows, cols = bounds
    aa: coords = (0, 0)
    zz: coords = (0, 0)
    pairs: dict[str, list[Position]] = defaultdict(list)
    for row in range(1, rows-1):
        for col in range(1, cols-1):
            char = grid[row][col]
            if char != '.': continue 
            (uy,ux),(ly,lx),(ry,rx),(dy,dx) = surround4((row,col))
            name = ''
            level = 0
            if isLetter(grid[uy][ux]):
                name = grid[uy-1][ux] + grid[uy][ux]
                level = 1 if insideBounds((uy-2,ux), bounds) else -1
            elif isLetter(grid[dy][dx]):
                name = grid[dy][dx] + grid[dy+1][dx]
                level = 1 if insideBounds((dy+2,dx), bounds) else -1
            elif isLetter(grid[ly][lx]):
                name = grid[ly][lx-1] + grid[ly][lx]
                level = 1 if insideBounds((ly,lx-2), bounds) else -1
            elif isLetter(grid[ry][rx]):
                name = grid[ry][rx] + grid[ry][rx+1]
                level = 1 if insideBounds((ry, rx+2), bounds) else -1

            if name == '':
                continue 
            elif name == 'AA':
                aa = (row,col)
            elif name == 'ZZ':
                zz = (row,col)
            else:
                pairs[name].append(((row,col), level))


    portals: dict[coords, Position] = {}
    for group in pairs.values():
        (p1, l1), (p2,l2) = group 
        portals[p1] = (p2, l1)
        portals[p2] = (p1, l2)

    return aa, zz, portals

if __name__ == '__main__':
    do(solve, 19, 20)

'''
Part1:
- Analyze the grid to find the position of AA, ZZ and the portals:
    - Scan from row = 1 to numRows-1, col = 1 to numCols-1
    - Only consider empty spaces; look at their surround4 (UDLR)
    - If it has a letter neighbor, read the name by extending (U/D/L/R)
    - If the name is AA or ZZ, set the position of AA / ZZ 
    - Otherwise, it is a portal, and we'll pair it with the other position that has same name
- Use BFS to traverse the grid starting from AA until we find ZZ
- At each step, check the 4 neighbors (UDLR); additionally if there is a portal in the current
  position, we also add the portal's pair to the next possible coords
- Only consider neighbors that are free (.) and not yet visited; increment the steps for the neighbors
- Output the number of steps when we found ZZ

Part2:
- Similar to Part 1, but now the grid is multi-level and portals can take you above/below current level
- Analyze the grid similar to Part 1, but with few modifications:
    - We distinguish between portals on the inner edge (takes you 1 level down) vs outer edge (takes you 1 level up)
    - Portals now tell you what position it goes to next and the level adjustment (+1/-1)
- Still use BFS similar to Part 1, but with few modifications:
    - Start at AA, level 0 and goal is to get to ZZ, level 0
    - Visited set now contains the coords and the level, not just the coords (could be visited in another level)
    - The next positions could be the surround4 on the same level or if there is a portal on the current coords, 
      we can take it to the portal's next position with the level adjusted (+1/-1)
    - However, if using portals, check that it is not on level 0 and going higher (outer portals dont work on lvl 0 as it's highest)
'''