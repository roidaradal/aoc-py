# Advent of Code 2022 Day 14
# John Roy Daradal 

from aoc import *

Line = list[coords]

def data(full: bool) -> list[Line]:
    def fn(line) -> Line:
        points: Line = []
        for p in splitStr(line ,'->'):
            x,y = toInt2(p, ',')
            points.append((y,x))
        return points
    return [fn(line) for line in readLines(22, 14, full)]

def solve() -> Solution:
    rocks = data(full=True)

    # Part 1
    cave, caveFloor = createCave(rocks)
    rest1 = 0
    while True:
        settled = dropSand(cave, caveFloor, False)
        if settled:
            rest1 += 1
        else:
            break

    # Part 2 
    cave, caveFloor = createCave(rocks)
    caveFloor += 2 
    rest2 = 0 
    while True:
        dropSand(cave, caveFloor, True)
        rest2 += 1
        if cave[sandSource] == SAND:
            break 
    
    return newSolution(rest1, rest2)

AIR, SAND, ROCK = 0, 1, 2 
sandSource = (0,500)

def createCave(rocks: list[Line]) -> tuple[dict[coords,int], int]:
    cave: dict[coords,int] = defaultdict(int)
    for line in rocks:
        for i in range(len(line)-1):
            (y1,x1), (y2,x2) = line[i], line[i+1]
            if y1 == y2:
                x1, x2 = sorted([x1, x2])
                for x in range(x1,x2+1):
                    cave[(y1,x)] = ROCK
            elif x1 == x2:
                y1, y2 = sorted([y1, y2])
                for y in range(y1,y2+1):
                    cave[(y,x1)] = ROCK
    caveFloor = max(c[0] for c in cave.keys())
    return cave, caveFloor

def dropSand(cave: dict[coords,int], caveFloor: int, hasFloor: bool) -> bool:
    sand = sandSource
    deltas = [D, SW, SE]
    d, limit = 0, len(deltas)
    while True:
        nxt = move(sand, deltas[d])
        nxtDepth = nxt[0]
        if (hasFloor and nxtDepth == caveFloor) or (cave[nxt] == SAND or cave[nxt] == ROCK):
            d += 1 # go to next delta
            if d == limit:
                cave[sand] = SAND
                return True # rested
        elif cave[nxt] == AIR:
            sand = nxt
            d = 0 # go back to first delta
            if nxtDepth > caveFloor:
                return False # free-falling

if __name__ == '__main__':
    do(solve, 22, 14)

'''
Solve:
- Create the cave grid from the rock lines; determine the cave floor level 
- For Part 1, count the number of settled sand before a dropped sand free falls to the abyss
  (set hasFloor to False to indicate that you can fall below the floor level)
- For Part 2, the concrete cave floor is 2 levels below the max rock depth;
  Count the number of settled sand before the sand source at (0,500) is filled with sand stopping the flow

CreateCave:
- Go through each rock lines 
- A rock line is a list of coords that indicate the start - end of a line of rocks 
- Process the coordinates in pairs:
    - If pair has same y, we fill rocks horizontally 
    - If pair has same x, we fill rocks vertically
- Also compute the cave floor (maximum rock depth / y-axis)

DropSand:
- Sand starts at source (0,500)
- Loop through the 3 deltas: D, SW, SE by using the delta index d (start at 0)
- Move the sand using the current delta 
- If has concrete floor (Part 2) and the next y is the cave floor, it is blocked
- Or, if the next position is Sand or Rock, it is also blocked
- If blocked, increment the delta index to try another way
- But if the delta index reaches the limit (tried all 3), then the sand rests here 
- Otherwise, if the next position is air, we can move the sand here, reset the d index to 0
- If the next depth exceeds the cave floor, then the sand is free-falling
'''