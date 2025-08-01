# Advent of Code 2017 Day 21
# John Roy Daradal 

from aoc import *

Grid = list[str]
Pair = tuple[Grid, Grid]
gridVersions: dict[str, list[Grid]] = {}

def data(full: bool) -> tuple[list[Pair], list[Pair]]:
    map2: list[Pair] = []
    map3: list[Pair] = []
    for line in readLines(17, 21, full):
        key, value = splitStr(line, '=>')
        keyGrid: Grid = splitStr(key, '/')
        repGrid: Grid = splitStr(value, '/')
        if len(keyGrid) == 2:
            map2.append((keyGrid, repGrid))
        else:
            map3.append((keyGrid, repGrid))
    return map2, map3 

def solve() -> Solution:
    global gridVersions
    map2, map3 = data(full=True)
    # Compute grid versions 
    for keyGrid, _ in map2 + map3:
        key = gridState(keyGrid)
        gridVersions[key] = computeGridVersions(keyGrid)

    # Part 1 
    count1 = transformGrid(map2, map3, 5)

    # Part 2
    count2 = transformGrid(map2, map3, 18)

    return newSolution(count1, count2)

def transformGrid(map2: list[Pair], map3: list[Pair], rounds: int) -> int:
    grid: Grid = [
        '.#.',
        '..#',
        '###',
    ]
    for _ in range(rounds):
        grid = nextGrid(grid, map2, map3)

    return countOn(grid)

def gridState(grid: Grid) -> str:
    return '/'.join(grid)

def flipVertical(grid: Grid) -> Grid:
    return [grid[i] for i in range(len(grid)-1, -1, -1)]

def flipHorizontal(grid: Grid) -> Grid:
    return [line[::-1] for line in grid]

def rotateCW(grid: Grid) -> Grid:
    rows, cols = getBounds(grid)
    grid2: Grid = []
    for col in range(cols):
        line = [grid[row][col] for row in range(rows-1, -1, -1)]
        grid2.append(''.join(line))
    return grid2

def computeGridVersions(grid: Grid) -> list[Grid]:
    versions: set[str] = set()
    v0 = grid 
    v1 = flipVertical(v0)
    v2 = flipHorizontal(v0)
    v3 = flipVertical(v2)
    for v in [v0, v1, v2, v3]:
        versions.add(gridState(v))
        prev = v 
        for _ in range(3):
            rot = rotateCW(prev)
            versions.add(gridState(rot))
            prev = rot

    return [splitStr(state, '/') for state in versions]

def countOn(grid: Grid) -> int:
    count = 0 
    for line in grid:
        for tile in line:
            if tile == '#':
                count += 1
    return count

def nextGrid(grid: Grid, map2: list[Pair], map3: list[Pair]) -> Grid:
    rows, cols = getBounds(grid)
    numCols = 0
    subGrids: list[Grid] = []
    if rows % 2 == 0:
        subGrids = [findMatch(subGrid, map2) for subGrid in divideGrid(grid, 2)]
        numCols = cols // 2
    elif rows % 3 == 0:
        subGrids = [findMatch(subGrid, map3) for subGrid in divideGrid(grid, 3)]
        numCols = cols // 3

    grid2 = mergeGrid(subGrids, numCols)
    return grid2

def divideGrid(grid: Grid, size: int) -> list[Grid]:
    rows, cols = getBounds(grid)
    subGrids: list[Grid] = []
    for row in range(0, rows, size):
        for col in range(0, cols, size):
            subGrid: Grid = [grid[r][col:col+size] for r in range(row,row+size)]
            subGrids.append(subGrid)
    return subGrids

def findMatch(grid: Grid, pairs: list[Pair]) -> Grid:
    for keyGrid, repGrid in pairs:
        if isMatch(keyGrid, grid):
            return repGrid
    return []

def isMatch(keyGrid: Grid, grid: Grid) -> bool:
    key = gridState(keyGrid)
    for version in gridVersions[key]:
        if version == grid:
            return True 
    return False

def mergeGrid(subGrids: list[Grid], size: int) -> Grid:
    rows = len(subGrids[0])
    grid: Grid = []
    rowGrid: Grid = [''] * rows
    count = 0
    for subGrid in subGrids:
        for i in range(len(subGrid)):
            rowGrid[i] += subGrid[i]
        count += 1 
        if count == size:
            for line in rowGrid: 
                grid.append(line)
            count = 0
            rowGrid = [''] * rows
    return grid

if __name__ == '__main__':
    do(solve, 17, 21)

'''
Solve:
- Separate the grid mapping of 2x2 and 3x3 grids 
- For each key grid that can be mapped, compute its versions:
    - Four main versions: original, flip vertical, flip horizontal, flip vertical+horizontal
    - For each of the main version, rotate 90 degrees 3x 
    - Only keep the unique set of versions
- Starting from the initial grid, transform the grid for the given number of iterations:
    - If grid rows are divisible by 2, divide grid into 2x2 subgrids
    - If grid rows are divisible by 3, divide grid into 3x3 subgrids
    - Find the corresponding translation for each subgrid, using map2 or map3 
    - Go through each keyGrid => replacementGrid pairs of size 2x2 or 3x3
    - Check if the current subGrid matches any of the keyGrid's versions
    - Merge the subgrids back into one grid
- For Part 1, count the '#' pixels after 5 iterations 
- For Part 2, count the '#' pixels after 18 iterations
'''