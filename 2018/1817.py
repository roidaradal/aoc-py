# Advent of Code 2018 Day 17
# John Roy Daradal 

from aoc import *

Line = tuple[int2,int2] # y-range, x-range

def data(full: bool) -> list[Line]:
    def fn(line: str) -> Line:
        parts = sorted(splitStr(line, ',')) # x=, y=
        p1, p2 = parts
        p1 = p1.strip('x=')
        p2 = p2.strip('y=')
        return createRange(p2), createRange(p1)
    return [fn(line) for line in readLines(18, 17, full)]

def createRange(line: str) -> int2:
    if '..' in line:
        start, end = toInt2(line, '..')
        return (start,end+1)
    else:
        start = int(line)
        return (start,start+1)

def solve() -> Solution:
    lines = data(full=True)
    ground = Ground(lines)

    while True:
        canFlow = ground.dropWater(waterSource)
        if canFlow: break

    # Part 1 
    visited = ground.validVisited

    # Part 2
    water = ground.waterCount

    return newSolution(visited, water)


SAND, WATER, CLAY = 0, 1, 2
waterSource = (0,500)

class Ground:
    def __init__(self, lines: list[Line]):
        self.grid: dict[coords,int] = defaultdict(int)
        self.visited: set[coords] = set()

        for ((y1,y2),(x1,x2)) in lines:
            for y in range(y1, y2):
                for x in range(x1, x2):
                    self.grid[(y,x)] = CLAY 
        
        ys = [c[0] for c in self.grid.keys()]
        xs = [c[1] for c in self.grid.keys()]
        self.ymin = min(ys)
        self.ymax = max(ys)
        self.xmin = min(xs)
        self.xmax = max(xs)

    def __getitem__(self, key: coords) -> int:
        return self.grid[key]
    
    def __setitem__(self, key: coords, tile: int):
        self.grid[key] = tile

    def display(self):
        ymin = min(0, self.ymin)
        for y in range(ymin, self.ymax+3):
            line: list[str] = []
            for x in range(self.xmin-1, self.xmax+2):
                pt = (y,x)
                tile = '.'
                if pt == waterSource:
                    tile = '+'
                elif self.grid[pt] == WATER:
                    tile = '~'
                elif self.grid[pt] == CLAY:
                    tile = '#'
                line.append(tile)
            print(''.join(line))

    @property
    def validVisited(self) -> int:
        return sum(1 for y,_ in self.visited if self.ymin <= y and y <= self.ymax)
    
    @property
    def waterCount(self) -> int:
        return sum(1 for tile in self.grid.values() if tile == WATER)

    def dropWater(self, water: coords) -> bool:
        water, canFlow = self.flowDown(water)
        if canFlow:
            # Infinite falling
            return True
        
        water1, canFlow1 = self.flowLeft(water)
        water2, canFlow2 = self.flowRight(water)
        
        if (not canFlow1) and (not canFlow2): # stuck on this level
            if water1 != water:
                water = water1 # go left 
            elif water2 != water:
                water = water2 # go right 
            self.grid[water] = WATER

        if canFlow1:
            canFlow1 = self.dropWater(water1)
        if canFlow2:
            canFlow2 = self.dropWater(water2)

        return canFlow1 or canFlow2

    # Note: flowX methods return ending position and canFlow flag
    # canFlow = False => stuck/settled
    # canFlow = True  => continue flowing down

    # Go down until hit clay/water or falls infinitely
    def flowDown(self, water: coords) -> tuple[coords, bool]:
        while True:
            down = move(water, D)
            if self.grid[down] == SAND: # free space to move
                self.visited.add(down)
                water = down 
                if water[0] > self.ymax: # exceeds ground floor
                    return water, True
            else: # blocked by CLAY/WATER below
                return water, False

    # Go left until hit clay/water or can go down one level
    def flowLeft(self, water: coords) -> tuple[coords, bool]:
        left = move(water, L)
        if self.grid[left] == SAND: # free space to move
            self.visited.add(left)
            leftDown = move(left, D) # try to go down 
            if self.grid[leftDown] == SAND: 
                # can go down one level: stop here
                self.visited.add(leftDown)
                return leftDown, True
            else:
                # cant go down, continue to left
                return self.flowLeft(left)
        else: # CLAY/WATER blocking left side 
            return water, False
        
    # Go right until hit clay/water or can go down one level 
    def flowRight(self, water: coords) -> tuple[coords, bool]:
        right = move(water, R)
        if self.grid[right] == SAND: # free space to move 
            self.visited.add(right)
            rightDown = move(right, D) # try to go down
            if self.grid[rightDown] == SAND:
                # can go down one leve: stop here
                self.visited.add(rightDown)
                return rightDown, True
            else:
                # cant go down, continue to right 
                return self.flowRight(right)
        else: # CLAY/WATER blocking right side 
            return water, False

if __name__ == '__main__':
    do(solve, 18, 17)

'''
Solve:
- Build the ground grid by adding the clay lines from input 
- Simulate dropping water from the water source (0,500) and see where it settles:
    - Make the water repeatedly flow down until it either hits clay/water (stop) or 
      has exceeded the ground floor (free-falling)
    - If flowDown indicated that we are free-falling, we stop here and indicate free-fall (True)
    - If cannot flow down further, water flows left and right
    - For flow left/right, we keep moving left/right until we either:
        - hit clay/water blocking left/right side  
        - found a space to go down to
        - Return the last coordinate (leftmost/rightmost or down) and whether succeeded to go down or not
    - If after checking the left and right flow, both indicated that they are stuck:
        - We check first if we can assign water to the leftmost (not same as current position)
        - Otherwise, we check if we can assign water to rightmost (not same as current position)
        - Last resort, water settles at current spot
        - Update the grid with water on where it settles (leftmost/rightmost/current)
    - If it can still flow to the left, recursively call dropWater starting with the leftDown position
    - If it can still flow to the right, recursively call dropWater starting with the rightDown position
    - The drop can still flow if either of left/right flow can still continue
- During the simulation, keep track of visited tiles
- Stop the loop if the water is free-falling
- For Part 1, count the visited tiles that are within y-range of the grid 
- For Part 2, count the settled water in the ground
'''