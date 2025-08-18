# Advent of Code 2021 Day 23
# John Roy Daradal 

import heapq
from aoc import *

State = tuple[int, str] # cost, gridState
Pod = tuple[coords, str]
MovePod = tuple[coords, str, bool] # position, name, goingHome 
Grid = list[list[str]]

goalOf: dict[str, list[coords]] = {
    'A': [(2,3),(3,3)],
    'B': [(2,5),(3,5)],
    'C': [(2,7),(3,7)],
    'D': [(2,9),(3,9)],
}

goalOf2: dict[str, list[coords]] = {
    'A': [(2,3),(3,3),(4,3),(5,3)],
    'B': [(2,5),(3,5),(4,5),(5,5)],
    'C': [(2,7),(3,7),(4,7),(5,7)],
    'D': [(2,9),(3,9),(4,9),(5,9)],
}

stepCost: dict[str,int] = {
    'A' : 1,
    'B' : 10,
    'C' : 100,
    'D' : 1000,
}

pathCache: dict[tuple[coords,coords], list[coords]] = {}

FREE, WALL = '.', '#'

hallway: list[coords] = [(1,1),(1,2),(1,4),(1,6),(1,8),(1,10),(1,11)]

def data(full: bool) -> Grid:
    def fn(line: str) -> list[str]:
        line = line.strip('\n')
        return list(line)
    return [fn(line) for line in readLines(21, 23, full, strip=False)]

def solve() -> Solution:
    grid = data(full=True)

    # Part 1 
    minEnergy1 = arrangePods(grid, False)

    # Part 2 
    line1 = grid[-1][:]
    line2 = grid[-1][:]
    for idx,tile in [(3,'D'),(5,'C'),(7,'B'),(9,'A')]:
        line1[idx] = tile 
    for idx,tile in [(3,'D'),(5,'B'),(7,'A'),(9,'C')]:
        line2[idx] = tile 
    grid = grid[:-2] + [line1, line2] + grid[-2:]
    minEnergy2 = arrangePods(grid, True)

    return newSolution(minEnergy1, minEnergy2)

def arrangePods(grid: Grid, expanded: bool) -> int:
    goalGrid: str = createGoalGrid(grid, expanded)
    createPathCache(grid, expanded)

    pq: list[State] = []
    state: State = (0, gridState(grid))
    heapq.heappush(pq, state)

    sp: dict[str,int] = defaultdict(lambda: INF)
    while len(pq) > 0:
        state = heapq.heappop(pq)
        cost, flatGrid = state
        if flatGrid == goalGrid:
            return cost
        
        for branch in branchStates(state, expanded):
            cost2, grid2 = branch 
            if sp[grid2] > cost2: 
                sp[grid2] = cost2
                heapq.heappush(pq, branch)
    return 0

def gridCopy(grid: Grid) -> Grid:
    return [line[:] for line in grid]

def gridState(grid: Grid) -> str:
    return '\n'.join([''.join(line) for line in grid])

def stateGrid(state: str) -> Grid:
    return [list(line) for line in state.split('\n')]

def createGoalGrid(grid: Grid, expanded: bool) -> str:
    goalMap = goalOf2 if expanded else goalOf
    grid2: Grid = gridCopy(grid)
    for name in goalMap:
        for y,x in goalMap[name]:
            grid2[y][x] = name
    return gridState(grid2)

def createPathCache(grid: Grid, expanded: bool):
    global pathCache 
    pathCache = {}

    goalMap = goalOf2 if expanded else goalOf

    # Rooms to hallways 
    for column in goalMap:
        for start in goalMap[column]:
            for dest in hallway:
                pathCache[(start,dest)] = bfsShortestPath(grid, start, dest)
    
    # Hallways to rooms
    for start in hallway:
        for column in goalMap:
            for dest in goalMap[column]:
                pathCache[(start, dest)] = bfsShortestPath(grid, start, dest)

def branchStates(state: State, expanded: bool) -> list[State]:
    cost, flatGrid = state 
    grid = stateGrid(flatGrid)

    # Get movable room pods and hallway pods
    movePods: list[MovePod] = []
    movePods += getMovableRoomPods(grid, expanded)
    movePods += getMovableHallwayPods(grid, expanded)

    # Create destination hallways and destination rooms 
    destHallway, destRoom = getDestinations(grid, movePods, expanded)

    # Create branches
    branches: list[State] = []
    for curr, name, goingHome in movePods:
        if goingHome: # hallway to room
            dest = destRoom[name]
            path = pathCache[(curr, dest)]
            if not all(grid[y][x] == FREE for y,x in path): continue 
            cost2 = cost + (len(path) * stepCost[name])
            grid2 = nextGrid(grid, curr, dest)
            branches.append((cost2, grid2))
        else: # room to hallway
            for dest in destHallway:
                path = pathCache[(curr, dest)]
                if not all(grid[y][x] == FREE for y,x in path): continue
                cost2 = cost + (len(path) * stepCost[name])
                grid2 = nextGrid(grid, curr, dest)
                branches.append((cost2, grid2))

    return branches

def getMovableRoomPods(grid: Grid, expanded: bool) -> list[MovePod]:
    pods: list[MovePod] = []
    goalMap = goalOf2 if expanded else goalOf

    # Determine columns that can have movement
    # Heterogeneous (has pod of wrong type in column)
    columns: list[str] = []
    for column in goalMap:
        for y,x in goalMap[column]:
            tile = grid[y][x]
            if tile != column and tile != FREE:
                columns.append(column)
                break

    # Check topmost of each movable column
    for column in columns:
        for y,x in goalMap[column]:
            tile = grid[y][x]
            if tile != FREE: 
                pods.append(((y,x), tile, False))
                break

    return pods

def getMovableHallwayPods(grid: Grid, expanded: bool) -> list[MovePod]:
    pods: list[MovePod] = []
    goalMap = goalOf2 if expanded else goalOf

    # Determine columns that can accept from hallway
    # Homogeneous (all pods are correct type or empty)
    columns: list[str] = []
    for column in goalMap:
        items: set[str] = set()
        for y,x in goalMap[column]:
            tile = grid[y][x]
            if tile != FREE: items.add(tile)
        items.add(column) # add so empty columns have 1 item
        if len(items) > 1: continue 
        item = tuple(items)[0]
        if item == column:
            columns.append(column)

    # Check hallway pods whose goal columns can accept from hallway
    for y,x in hallway:
        tile = grid[y][x]
        if tile == FREE: continue 
        if tile not in columns: continue 
        pods.append(((y,x), tile, True))

    return pods

def getDestinations(grid: Grid, movePods: list[MovePod], expanded: bool) -> tuple[list[coords], dict[str,coords]]:
    goalMap = goalOf2 if expanded else goalOf 

    # Create destination hallways
    destHallway: list[coords] = [(y,x) for y,x in hallway if grid[y][x] == FREE]

    # Create destination rooms
    # Get columns that allow hallway pods to go home
    destColumns: set[str] = set()
    for _, column, goingHome in movePods:
        if not goingHome: continue 
        destColumns.add(column)
    # Find bottom-most free space in each destination column
    destRoom: dict[str, coords] = {}
    for column in destColumns:
        for y,x in reversed(goalMap[column]):
            if grid[y][x] == FREE:
                destRoom[column] = (y,x)
                break
    
    return destHallway, destRoom

def nextGrid(grid: Grid, curr: coords, dest: coords) -> str:
    grid2: Grid = gridCopy(grid)
    (y,x), (ny,nx) = curr, dest
    name = grid2[y][x]
    grid2[y][x] = FREE 
    grid2[ny][nx] = name 
    return gridState(grid2)

def bfsShortestPath(grid: Grid, start: coords, goal: coords) -> list[coords]:
    q: list[list[coords]] = [[start]]
    done: set[coords] = set()
    while len(q) > 0:
        path = q.pop(0)
        curr = path[-1]
        if curr == goal: return path[1:] # dont include starting point

        if curr in done: continue 
        done.add(curr)

        for nxt in surround4(curr):
            ny,nx = nxt
            if grid[ny][nx] == WALL: continue
            if nxt in done: continue
            q.append(path + [nxt])
    return []

if __name__ == '__main__':
    do(solve, 21, 23)

'''
Solve: 
- The goalOf dictionary indicates the grid positions that we want the pod types to end up in 
- Keep a list of the allowed hallway positions (row 1, except for those on the room columns)
- Use Dijkstra's algorithm to find the minimum energy required to arrange the pods into their rooms:
    - Create the goal grid: the grid where all pod types are in their correct rooms; use this for stop condition
    - Pre-compute the shortest paths from the rooms to hallways and hallways to rooms, using BFS
    - Initialize the minimum energy for any grid state to INF (use defaultdict)
    - Once the current grid from the heap PQ is the goal grid, return the current cost 
    - Otherwise, try to create the branches from the current state
    - Add the branch to the PQ if the branch cost is lesser than the current sp[grid2]
- To get the branches from the current state:
    - Get pods that are currently in a room that can be moved into the hallway:
        - Determine columns that have wrong type of pod in it (only move in this column if needed)
        - Add the topmost of each movable column into the list of pods that can be moved (only the topmost can move)
    - Get pods that are currently in the hallway that can be moved into its room:
        - Determine columns that can accept pods from the hallway: either empty or all of correct type
        - Check the pods in the hallway whose goal column can accept from the hallway
    - Get the possible destination hallways and rooms:
        - Hallway positions that are currently free / not occupied by a pod 
        - Get columns that allow hallway pods to go home, and find the bottom-most free space in each column
    - Go through all the movable pods to check which are valid branches
    - If going from hallway to room, there is only one possible room destination (bottom-most FREE in that column)
    - If going from room to hallway, go through the possible destination hallways
    - Check that the cached path from the source to the destination is not obstructed (all FREE)
    - New cost of branch = current cost + path length * stepCost of pod type
    - The next grid is where the source pod has transferred to the destination, and the previous source spot is now free
- For Part 1, use the normal input grid
- For Part 2, augment the grid with 2 lines betwen the 2 original room rows: DCBA and DBAC
- Use a different goalOf dictionary for Part 2, where each room has 4 slots (goalOf2)
'''