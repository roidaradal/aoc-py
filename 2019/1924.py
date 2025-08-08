# Advent of Code 2019 Day 24
# John Roy Daradal 

from aoc import *

Grid = list[str]
RecGrid = dict[int3, bool] # (y,x,level)
MID = 2
SIDE = 5
OUT_NEG = -1
OUT_POS = SIDE
center: coords = (MID, MID)

def data(full: bool) -> Grid:
    return readLines(19, 24, full)

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    grid = data(full=True)
    bounds = getBounds(grid)

    done: list[str] = [gridState(grid)]
    while True:
        grid = nextGrid(grid, bounds)
        state = gridState(grid)
        if state in done: 
            rating = sum(2**i for i,tile in enumerate(state) if tile == '#')
            return rating
        done.append(state)

def part2() -> int:
    grid = data(full=True)

    recGrid: RecGrid = defaultdict(bool)
    for y,line in enumerate(grid):
        for x,tile in enumerate(line):
            if (y,x) == center: continue # skip center
            recGrid[(y,x,0)] = tile == '#'

    for _ in range(200):
        recGrid = nextRecGrid(recGrid)
    
    return sum(recGrid.values())

def gridState(grid: Grid) -> str:
    return ''.join(grid)

def nextGrid(grid: Grid, bounds: dims2) -> Grid:
    grid2: Grid = []
    for row,line in enumerate(grid):
        line2: list[str] = []
        for col,tile in enumerate(line):
            neighborBugs = 0
            for nxt in surround4((row,col)):
                if not insideBounds(nxt, bounds): continue
                ny,nx = nxt
                if grid[ny][nx] == '#': neighborBugs += 1 
            tile2 = tile 
            if tile == '#' and neighborBugs != 1:
                tile2 = '.'
            elif tile == '.' and neighborBugs in (1,2):
                tile2 = '#'
            line2.append(tile2)
        grid2.append(''.join(line2))
    return grid2

def nextRecGrid(recGrid: RecGrid) -> RecGrid:
    recGrid2: RecGrid = defaultdict(bool)
    levels: list[int] = sorted(set([k[2] for k in recGrid.keys()]))
    outer = min(levels) - 1 
    inner = max(levels) + 1 
    levels = [outer] + levels + [inner]
    for level in levels:
        for curr in gridKeys(level):
            y,x,l = curr
            neighborBugs = 0 
            for nxt in recursiveNeighbors(y, x, l):
                if recGrid[nxt]: neighborBugs += 1
            isBug = recGrid[curr] 
            isBug2 = isBug 
            if isBug and neighborBugs != 1:
                isBug2 = False 
            elif not isBug and neighborBugs in (1,2):
                isBug2 = True 
            recGrid2[curr] = isBug2
    return recGrid2

def gridKeys(level: int) -> list[int3]:
    keys: list[int3] = []
    for y in range(SIDE):
        for x in range(SIDE):
            if (y,x) == center: continue 
            keys.append((y,x,level))
    return keys

def recursiveNeighbors(y: int, x: int, level: int) -> list[int3]:
    neighbors: list[int3] = []
    curr: coords = (y,x)
    for d in [U,D,L,R]:
        nxt = move(curr, d)
        ny,nx = nxt
        if d == U and ny == OUT_NEG:    # top outer edge
            neighbors.append((MID-1, MID, level-1)) 
        elif d == D and ny == OUT_POS:  # bottom outer edge
            neighbors.append((MID+1, MID, level-1))
        elif d == L and nx == OUT_NEG:  # left outer edge 
            neighbors.append((MID, MID-1, level-1)) 
        elif d == R and nx == OUT_POS:  # right outer edge 
            neighbors.append((MID, MID+1, level-1))
        elif d == D and nxt == center:  # top inner edge 
            for nx in range(SIDE):
                neighbors.append((0, nx, level+1)) 
        elif d == U and nxt == center:  # bottom inner edge
            for nx in range(SIDE):
                neighbors.append((SIDE-1, nx, level+1))
        elif d == R and nxt == center:  # left inner edge 
            for ny in range(SIDE):
                neighbors.append((ny, 0, level+1)) 
        elif d == L and nxt == center:  # right inner edge 
            for ny in range(SIDE):
                neighbors.append((ny, SIDE-1, level+1))
        else: # normal neighbor, same level
            neighbors.append((ny, nx, level))

    return neighbors

if __name__ == '__main__':
    do(solve, 19, 24)

'''
Part1:
- Start with the initial grid
- Repeatedly transform the grid until we find a repeating grid:
    - For each tile, count the number of bugs in the 4 surrounding tiles (UDLR)
    - If bug tile (#) and neighborBugs != 1, tile becomes empty (.)
    - If empty tile (.) and neighborBugs is 1 or 2, tile becomes bug-infested (#)
- Keep track of done grid states (flatten grid into a single string)
- If we find a repeated state, compute the biodiversity rating:
    - Flatten the grid into a 1D array, go through the tiles with bugs (#)
    - Sum up the 2**idx of bug tiles

Part2:
- The recursion grid is a dictionary that maps (y,x,level) => bug (True/False)
- Use defaultdict so that unexplored (y,x,level) are initialized to False (bug-free)
- Add the bugs in the initial grid to level 0 on the recursion grid
- Update the recursion grid for 200 rounds:
    - Get the current levels in the recursion grid and sort them in ascending order
    - Add two levels in processing: minLevel-1 and maxLevel+1
    - This should expand the grid at each iteration, as there could be bugs in the min and max level
    - For each level in ascending order, go through the grid cells, except the center:
    - Get the recursive neighbors of this cell, and count the number of bugs from the neighbors
    - Tile transformation is similar to Part 1:
        - If bug tile and neighborBugs != 1, tile becomes empty 
        - If empty tile and neighborBugs is 1 or 2, tile becomes bug-infested
- To get the neighbor of (y,x) at level L:
    - Go through the 4 directions (UDLR) and get the next position for that direction
    - If neighbor goes out-of-bounds, go one level higher (level - 1)
        - If d=U and ny=-1 (top outer edge),  add (1,2,L-1) as neighbor
        - If d=D and ny=5  (bot outer edge),  add (3,2,L-1) as neighbor
        - If d=L and nx=-1 (left outer edge), add (2,1,L-1) as neighbor
        - If d=R and nx=5 (right outer edge), add (2,3,L-1) as neighbor
    - If neighbor goes to center (2,2), go one level deeper (level + 1) and add 4 neighbors:
        - If d=D (top inner edge),   add (0,x,L+1) for x=0..4
        - If d=U (bot inner edge),   add (4,x,L+1) for x=0..4
        - If d=R (left inner edge),  add (y,0,L+1) for y=0..4
        - If d=L (right inner edge), add (y,4,L+1) for y=0..4
    - Otherwise, add neighbor on the same level
- Output the number of bugs in the grid after 200 rounds
'''