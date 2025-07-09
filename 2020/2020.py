# Advent of Code 2020 Day 20
# John Roy Daradal 

from aoc import do, readLines, newSolution, Solution
from aoc import getBounds, coords, int2, defaultdict

Grid = list[str]
Perimeter = dict[int, str]
Layout = dict[int, int2]    # {position => (gridName, gridVersion)}
GridVersions = dict[int, dict[int, Grid]]       # {gridName => {version: Grid}}
GridEdges = dict[int, dict[int, Perimeter]]     # {gridName => {version: Perimeter}}
GridZones = dict[int, dict[int, list[Layout]]]  # {gridName => {version: []Layout}}
FromTo = tuple[int2, int2]  # ((fromName, fromVersion), (toName, toVersion))

C, T, R, B, L = 0, 1, 2, 3, 4
TR, BR, BL, TL = 5, 6, 7, 8
OPP = {T: B, B: T, L: R, R: L}

TLC, TRC, BRC, BLC = 0, 1, 2, 3
TE, RE, BE, LE, IN = 4, 5, 6, 7, 8

def data(full: bool) -> dict[int, Grid]:
    grids: dict[int, Grid] = {}
    name: int = 0 
    grid: Grid = []
    for line in readLines(20, 20, full):
        if line.startswith('Tile'):
            name =int(line.strip(':').split()[1])
        elif line == '':
            grids[name] = grid 
            grid = []
        else:
            grid.append(line)
    grids[name] = grid
    return grids

def solve() -> Solution:
    grids = data(full=True)

    # Part 1
    gridVersions: GridVersions = {}
    gridEdges: GridEdges = {}
    for name, grid in grids.items():
        gridVersions[name] = getGridVersions(grid)
        gridEdges[name] = getGridEdges(gridVersions[name])

    gridZones: GridZones = {}
    insideZones: list[int] = []
    for name in grids:
        gridZones[name] = getValidZones(gridEdges, name)
        if IN in gridZones[name]:
            insideZones.append(name)

    name = insideZones[0]
    layout = gridZones[name][IN][0]
    fullGrid = expandGrid(layout, gridZones)

    ys = set([c[0] for c in fullGrid.keys()])
    xs = set([c[1] for c in fullGrid.keys()])
    minY, minX = min(ys), min(xs)
    maxY, maxX = max(ys), max(xs)
    cor1 = fullGrid[(minY, minX)][0]
    cor2 = fullGrid[(minY, maxX)][0]
    cor3 = fullGrid[(maxY, minX)][0]
    cor4 = fullGrid[(maxY, maxX)][0]
    product = cor1*cor2*cor3*cor4

    # Part 2
    img: Grid = []
    for row in range(minY, maxY+1):
        tiles: list[Grid] = []
        tileRows = 0
        for col in range(minX, maxX+1):
            name, version = fullGrid[(row, col)]
            tile = innerGrid(gridVersions[name][version])
            tileRows = len(tile)
            tiles.append(tile)
        for t in range(tileRows):
            line = [tile[t] for tile in tiles]
            img.append(''.join(line))

    score = 0
    for img in getGridVersions(img).values():
        score = findMonster(img)
        if score > 0: break

    return newSolution(product, score)

def gridState(grid: Grid) -> str:
    return ''.join(grid)

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

def topEdge(grid: Grid) -> str:
    return grid[0]

def bottomEdge(grid: Grid) -> str:
    return grid[-1]

def leftEdge(grid: Grid) -> str:
    return ''.join(line[0] for line in grid)

def rightEdge(grid: Grid) -> str:
    return ''.join(line[-1] for line in grid)

def getGridVersions(grid: Grid) -> dict[int, Grid]:
    group: dict[str, list[Grid]] = defaultdict(list)
    v0 = grid 
    v1 = flipVertical(v0)
    v2 = flipHorizontal(v0)
    v3 = flipVertical(v2)
    for v in [v0, v1, v2, v3]:
        group[gridState(v)].append(v)
        prev = v 
        for _ in range(3):
            rot = rotateCW(prev)
            group[gridState(rot)].append(rot)
            prev = rot
    i = 0
    versions: dict[int, Grid] = {}
    for key in sorted(group):
        versions[i] = group[key][0]
        i += 1
    return versions

def getGridEdges(versions: dict[int, Grid]) -> dict[int, Perimeter]:
    edges: dict[int, Perimeter] = {}
    for gridId, grid in versions.items():
        edges[gridId] = {
            T: topEdge(grid),
            R: rightEdge(grid), 
            B: bottomEdge(grid), 
            L: leftEdge(grid),
        }
    return edges

def getValidNeighbors(edges: GridEdges, name: int, direction: int, version: int|None=None) -> list[FromTo]:
    versionOptions: list[int] = list(edges[name].keys())
    if version != None:
        versionOptions = [version]
    oppDirection = OPP[direction]
    fromName = name 
    pairs: list[FromTo] = []
    for fromVersion in versionOptions:
        perimeter = edges[fromName][fromVersion]
        fromEdge = perimeter[direction]
        for toName in edges:
            if fromName == toName: continue 
            for toVersion, perimeter2 in edges[toName].items():
                toEdge = perimeter2[oppDirection]
                if fromEdge == toEdge:
                    pair: FromTo = ((fromName, fromVersion), (toName, toVersion))
                    pairs.append(pair)
    return pairs

def getValidLayouts(edges: GridEdges, name: int, direction1: int, direction2: int, direction3: int) -> list[Layout]:
    neighbors1 = getValidNeighbors(edges, name, direction1)
    neighbors2 = getValidNeighbors(edges, name, direction2)

    layouts: list[Layout] = []
    for (_, currVersion1), (adjName1, adjVersion1) in neighbors1:
        for (_, currVersion2), (adjName2, adjVersion2) in neighbors2:
            if currVersion1 != currVersion2: continue # skip if not same current version
            if adjName1 == adjName2: continue # skip if ajdacent1 and adjacent2 are same
            diag12 = [p[1] for p in getValidNeighbors(edges, adjName1, direction2, adjVersion1)]
            diag21 = [p[1] for p in getValidNeighbors(edges, adjName2, direction1, adjVersion2)]
            common = set(diag12).intersection(set(diag21))
            for (adjName3, adjVersion3) in common:
                if adjName3 in (name, adjName1, adjName2): continue 
                layout: Layout = {}
                layout[C] = (name, currVersion1)
                layout[direction1] = (adjName1, adjVersion1)
                layout[direction2] = (adjName2, adjVersion2)
                layout[direction3] = (adjName3, adjVersion3)
                layouts.append(layout)
    return layouts

def getValidZones(edges: GridEdges, name: int) -> dict[int, list[Layout]]:
    topRight = getValidLayouts(edges, name, T, R, TR)
    rightBot = getValidLayouts(edges, name, R, B, BR)
    botLeft  = getValidLayouts(edges, name, B, L, BL)
    leftTop  = getValidLayouts(edges, name, L, T, TL)
    
    zones: dict[int, list[Layout]] = {}

    # Corners
    if len(topRight) > 0:
        zones[BLC] = topRight
    if len(rightBot) > 0:
        zones[TLC] = rightBot
    if len(botLeft) > 0:
        zones[TRC] = botLeft
    if len(leftTop) > 0:
        zones[BRC] = leftTop

    # Edges 
    topEdge = checkOverlap(rightBot, botLeft, B)
    if len(topEdge) > 0: zones[TE] = topEdge

    botEdge = checkOverlap(leftTop, topRight, T)
    if len(botEdge) > 0: zones[BE] = botEdge

    leftEdge  = checkOverlap(topRight, rightBot, R)
    if len(leftEdge) > 0: zones[LE] = leftEdge

    rightEdge = checkOverlap(botLeft, leftTop, L)
    if len(rightEdge) > 0: zones[RE] = rightEdge

    # Inner 
    inner = checkInner(topRight, rightBot, botLeft, leftTop)
    if len(inner) > 0: zones[IN] = inner

    return zones

def checkInner(topRight: list[Layout], rightBot: list[Layout], botLeft: list[Layout], leftTop: list[Layout]) -> list[Layout]:
    layouts1 = topRight 
    overlaps = [R, B, L]
    for layouts2 in [rightBot, botLeft, leftTop]:
        overlap = overlaps.pop(0)
        overlapCount = 3 if overlap == L else 2
        layouts1 = checkOverlap(layouts1, layouts2, overlap, overlapCount)
        if len(layouts1) == 0: return []
    return layouts1

def checkOverlap(layouts1: list[Layout], layouts2: list[Layout], overlap: int, overlapCount: int = 2) -> list[Layout]:
    layouts3: list[Layout] = []
    for layout1 in layouts1:
        curr1 = layout1[C]
        nxt1 = layout1[overlap]
        for layout2 in layouts2:
            curr2 = layout2[C]
            nxt2 = layout2[overlap]
            if curr1 != curr2 or nxt1 != nxt2: continue
            if countLayoutIntersection(layout1, layout2) != overlapCount: continue 
            layout: Layout = {}
            layout.update(layout1)
            layout.update(layout2)
            layouts3.append(layout)
    return layouts3

def countLayoutIntersection(layout1: Layout, layout2: Layout) -> int:
    tiles1 = set([v[0] for v in layout1.values()])
    tiles2 = set([v[0] for v in layout2.values()])
    return len(tiles1.intersection(tiles2))

def expandGrid(firstLayout: Layout, gridZones: GridZones) -> dict[coords, int2]:
    fullGrid: dict[coords, int2] = {}

    layout = firstLayout
    aboveLayouts = expandLayout(layout, gridZones, T, IN, TE)[::-1]
    belowLayouts = expandLayout(layout, gridZones, B, IN, BE)
    
    colLayouts = aboveLayouts + [firstLayout] + belowLayouts 
    row, lastRow = 0, len(colLayouts) - 1
    for row, layout in enumerate(colLayouts):
        lzone1, lzone2 = IN, LE 
        rzone1, rzone2 = IN, RE 
        if row == 0:
            lzone1, lzone2 = TE, TLC 
            rzone1, rzone2 = TE, TRC 
        elif row == lastRow:
            lzone1, lzone2 = BE, BLC 
            rzone1, rzone2 = BE, BRC
        leftLayouts  = expandLayout(layout, gridZones, L, lzone1, lzone2)[::-1]
        rightLayouts = expandLayout(layout, gridZones, R, rzone1, rzone2)
        current  = [layout[C] for layout in leftLayouts]
        current += [layout[C]]
        current += [layout[C] for layout in rightLayouts]
        for col, center in enumerate(current):
            fullGrid[(row,col)] = center

    return fullGrid

def expandLayout(layout: Layout, gridZones: GridZones, direction: int, zone1: int, zone2: int) -> list[Layout]:
    currentTiles: dict[int2, list[int]] = {
        (T, IN) : [TL, T, TR, L, C, R],
        (B, IN) : [L, C, R, BL, B, BR],
        (L, IN) : [TL, L, BL, T, C, B],
        (R, IN) : [T, C, B, TR, R, BR],
        (L, TE) : [L, BL, C, B], 
        (R, TE) : [C, B, R, BR], 
        (L, BE) : [TL, L, T, C],
        (R, BE) : [T, C, TR, R],
    }
    nextTiles: dict[int2, list[int]] = {
        (T, IN) : [L, C, R, BL, B, BR],
        (B, IN) : [TL, T, TR, L, C, R],
        (L, IN) : [T, C, B, TR, R, BR],
        (R, IN) : [TL, L, BL, T, C, B],
        (L, TE) : [C, B, R, BR], 
        (R, TE) : [L, BL, C, B],
        (L, BE) : [T, C, TR, R], 
        (R, BE) : [TL, L, T, C],
    }
    key = (direction, zone1)

    nextLayouts: list[Layout] = []
    while True:
        current = tuple(layout[d] for d in currentTiles[key])
        zone, foundEnd = zone1, False
        nxtName = layout[direction][0]
        if zone not in gridZones[nxtName]:
            zone, foundEnd = zone2, True 
        
        foundMatch = False 
        for layout2 in gridZones[nxtName][zone]:
            nxt = tuple(layout2[d] for d in nextTiles[key])
            if current == nxt:
                nextLayouts.append(layout2)
                layout = layout2 
                foundMatch = True 
                break 
        
        if foundEnd or not foundMatch: break 
    return nextLayouts

def innerGrid(grid: Grid) -> Grid:
    rows, cols = getBounds(grid)
    return [grid[row][1:cols-1] for row in range(1, rows-1)]

def findMonster(grid: Grid) -> int:
    monster: Grid = [
        '------------------#-',
        '#----##----##----###',
        '-#--#--#--#--#--#---',
    ]
    gridRows, gridCols = getBounds(grid)
    windowRows, windowCols = getBounds(monster)

    hasMonster: set[coords] = set()
    for row in range(0, gridRows-windowRows):
        for col in range(0, gridCols-windowCols):
            gridWindow: Grid = [grid[r][col:col+windowCols] for r in range(row, row+windowRows)]
            ok, matches = matchMonster(gridWindow, monster)
            if not ok: continue
            for r,c in matches:
                hasMonster.add((row+r, col+c))

    if len(hasMonster) == 0:
        return 0
    else:
        count = sum(sum(1 for x in line if x == '#') for line in grid)
        return count - len(hasMonster)

def matchMonster(window: Grid, monster: Grid) -> tuple[bool, list[coords]]:
    matches: list[coords] = []
    for row in range(len(window)):
        line1, line2 = window[row], monster[row]
        col = 0
        for w,m in zip(line1, line2):
            if m == '#' and w != m:
                return False, []
            elif m == '#' and w == m:
                matches.append((row,col))
            col += 1
    return True, matches

if __name__ == '__main__':
    do(solve, 20, 20)

'''
Part1:
- For each grid, create the 8 versions by flipping vertically/horizontally and rotating the grids
- For each grid version, extract the top, bottom, left and right edges for matching later
- For each grid, get their valid zones (areas where they could be placed): IN, (T|B|L|R)E, (TL|TR|BL|BR)C
    - Get the valid layouts for topRight, rightBot, botLeft, and leftTop 
    - Corner zone if it has non-empty topRight (BLC), rightBot (TLC), botLeft (TRC), or leftTop (BRC)
    - Edge zone if has non-empty overlaps for:
        - rightBot + botLeft => TE 
        - leftTop + topRight => BE 
        - topRight + rightBot => LE 
        - botLeft + leftTop  => RE
    - Inner zone if has non-empty overlap for the full chain: topRight+rightBot+botLeft+leftTop
- To get valid layout for dir1, dir2 converging into dir3:
    - Get the valid neighbors of current tile in direction1 and 2
    - Find the overlap in neighbors such that the current grid's version is consistent and the adjacent tiles are different
    - Get the diagonal of the 2 neighbors pointing into direction3 
    - Process the overlap of the 2 neighbors' diagonals and create layouts
- To get valid neighbors of a grid in certain direction:
    - Can go through all versions of the grid or only certain version
    - Go through the list of grid versions (1 or all), prepare the edge in the direction specified 
    - Go through the other grid's edges (skip current grid), and find a match of the current edge
      from the other grid's opposition direction (e.g. if looking for top, check other grid's bottom)
- Use the first grid that can be inside the grid (not in corners or edges); use its first layout 
- Expand the full grid from this first inner grid
    - From the inner layout, expand above and below => this forms a full column 
    - Combine the reversed above layouts + current layout + below layouts
    - For each layout, expand to the left and right, building the full grid incrementally
    - To expand layout in a direction, continue along the initial zone until we cant anymore (reached edge/corner)
    - Prepare the current layout's part that will overlap with the next 
    - Check the layouts of the grid on the given direction, and extract the part which will overlap with the current
    - If the current and next layout's overlapping parts match, we have found the next layout 
    - Continue until we have not found a match or have reached the end (edge/corner)
- After computing the full grid, get the grid IDs of the 4 corners, and return their product

Part2:
- From the full grid in Part 1, build the image by using the grid name and version at particular cells
- Only use the inner grid from the original grids (remove edges)
- Go through the 8 versions of the image, and check if we can find the sea monster
- Use sliding window to check if the grid window matches with the monster window
- During matching, we only compare if the monster window has # tile
- Once we find the sea monster, return the number of # in the grid not touched by the monster
'''