# Advent of Code 2022 Day 17
# John Roy Daradal 

from aoc import *

Grid = dict[coords, str]
Rock = list[str]
GridTop = tuple[int, ...]

rocks: list[Rock] = [
    [
        '####',
    ],
    [
        '.#.',
        '###',
        '.#.',
    ],
    [
        '..#',
        '..#',
        '###',
    ],
    [
        '#',
        '#',
        '#',
        '#',
    ],
    [
        '##',
        '##',
    ]
]

FLOOR: int = 0
WIDTH: int = 7

def data(full: bool) -> list[delta]:
    T: dict[str, delta] = {'<': L, '>': R}
    return [T[x] for x in readFirstLine(22, 17, full)]

def solve() -> Solution:
    jets = data(full=True)
    grid: Grid = defaultdict(lambda: '.')
    rockIdx, jetIdx = 0, 0
    numRocks = len(rocks)
    ymin = FLOOR

    results: list[GridTop] = [gridTop(grid, rockIdx, jetIdx)]
    ydiffs: list[int] = [0]
    idx, loopLength = 0, 0

    while True:
        yprev = ymin
        jetIdx, ymin = dropRock(grid, jets, jetIdx, rockIdx, ymin)
        rockIdx = (rockIdx + 1) % numRocks
        ydiff = yprev - ymin
        
        state = gridTop(grid, rockIdx, jetIdx)
        if state in results:
            idx = results.index(state)
            loopLength = len(results) - idx
            break

        results.append(state)
        ydiffs.append(ydiff)
        
    # Part 1 and 2
    heights = []
    rounds1 = 2022 
    rounds2 = 1_000_000_000_000
    for rounds in [rounds1, rounds2]:
        rounds = (rounds+1) - idx # remove loop prefix 
        loopCount = rounds // loopLength 
        loopIdx = rounds % loopLength 

        prefixHeight = sum(ydiffs[:idx]) # height before the loop 
        loopHeight = sum(ydiffs[idx:])
        extraHeight = sum(ydiffs[idx: idx+loopIdx])
        height = prefixHeight + (loopCount * loopHeight) + extraHeight 
        heights.append(height)
    
    height1, height2 = heights
    
    return newSolution(height1, height2)

def dropRock(grid: Grid, jets: list[delta], jetIdx: int,  rockIdx: int, ymin: int) -> int2:
    numJets = len(jets)
    rock = rocks[rockIdx]
    rockBounds = getBounds(rock)

    rockHeight = rockBounds[0]
    topRow = (ymin-4) - (rockHeight-1)
    currTopLeft: coords = (topRow, 2)
    
    while True:
        # Jet stream moves the rock left/right
        topLeft = move(currTopLeft, jets[jetIdx])
        jetIdx = (jetIdx + 1) % numJets

        # Check if new rock position is collision-free
        if hasNoCollision(grid, rock, topLeft, rockBounds):
            currTopLeft = topLeft

        # Rock falls down 
        topLeft = move(currTopLeft, D)

        # Check if new rock position is collision-free 
        if hasNoCollision(grid, rock, topLeft, rockBounds):
            currTopLeft = topLeft 
        else:
            # Has collision on going down = settle rock here
            settleRock(grid, rock, currTopLeft, rockBounds)
            
            # Update ymin
            y = currTopLeft[0]
            ymin = min(ymin, y)
            break

    return jetIdx, ymin

def bottomRightOf(topLeft: coords, bounds: dims2) -> coords:
    (y1, x1), (h, w) = topLeft, bounds 
    return (y1 + h, x1 + w)

def hasNoCollision(grid: Grid, rock: Rock, topLeft: coords, rockBounds: dims2) -> bool:
    botRight = bottomRightOf(topLeft, rockBounds)
    (y1, x1), (y2, x2) = topLeft, botRight 
    
    # Check left wall
    if x1 < 0: 
        return False 
    
    # Check right wall 
    if x2 > WIDTH:
        return False 

    # Check floor 
    if y2 > FLOOR:
        return False 

    # Check collision
    for row, y in enumerate(range(y1, y2)):
        for col, x in enumerate(range(x1, x2)):
            rockTile = rock[row][col]
            gridTile = grid[(y,x)]
            if rockTile == '#' and gridTile == '#':
                return False
            
    return True 

def settleRock(grid: Grid, rock: Rock, topLeft: coords, rockBounds: dims2):
    botRight = bottomRightOf(topLeft, rockBounds)
    (y1, x1), (y2, x2) = topLeft, botRight 
    for row, y in enumerate(range(y1, y2)):
        for col, x in enumerate(range(x1, x2)):
            if rock[row][col] == '#':
                grid[(y,x)] = '#'

def gridTop(grid: Grid, rockIdx: int, jetIdx: int) -> GridTop:
    top: list[int] = [FLOOR] * WIDTH
    for (y,x), tile in grid.items():
        if tile == '#':
            top[x] = min(top[x], y)
    minTop = min(top)
    top = [x - minTop for x in top]
    top.append(rockIdx)
    top.append(jetIdx)
    return tuple(top)   

if __name__ == '__main__':
    do(solve, 22, 17)

'''
Solve:
- Use a defaultdict for the grid, which defaults to '.'
- Start with rockIdx = 0, jetIdx = 0, ymin = FLOOR (0)
- After dropping each rock, keep track of two things:
    - grid states: contour of the topmost floor/rock on each column, next rockIdx that will fall,
      and the next jetIdx that will affect the rock
    - ydiffs: difference of the previous ymin and the current ymin
- To compute the gridTop, initialize the tops of the 7 columns to the FLOOR (0)
- Go through all the # tiles in the grid
- Update the top of that column with the tile's y coord if better than current
- Normalize the values by taking their difference from the minimum top value
- We also add the rockIdx and jetIdx to the tuple as it is part of the whole state
- Initially, without rocks, we start with the gridTop of pure 0s (0s for gridTop, 0s for rockIdx, jetIdx)
  and ydiff of 0 (just to align the count of results and ydiffs)
- Since Part 2 is asking to repeat this 1 trillion times, this signals that the process involves finding a loop in the states
- Repeat these until we find a repeating state:
    - Drop the current rock (using rockIdx); this updates the ymin and the jetIdx 
    - We increment the rockIdx, wrapping around to the start if necessary
    - Get the ydiff: prev ymin and current ymin's difference: this tells us how much the ymin changes per round
    - Compute the grid state by finding the gridTop with the rockIdx and jetIdx
    - If this state has already been encountered previously, we stop as we have found the state loop
        - Find the index where the state first appeared 
        - The loop length is the number of results so far - index where state first appeared
    - Otherwise, we save the state and ydiff to their respective lists
- After finding the state loop, we find the height for the given number of rocks 
- Adjust the number of rounds by doing (rounds+1) - idx: +1 since we added the 0 values, -idx to remove the loop prefix 
- The remaining rounds count is the looped part:
    - Number of loops = rounds // loopLength = how many times do we repeat the loop
    - Loop Index = rounds % loopLength = after repeating the loops, which part of the loop do we stop?
- Compute the prefix height: sum of ydiffs up to the idx (height before the loop)
- One loop's height is the sum of ydiffs from idx up to the end (since we stopped adding to ydiffs when we found the loop)
- Total height for the loop part is loopHeight * loopCount 
- Then for the tail end, we add the extra height: sum of ydiffs from idx up to idx+loopIdx
- The total height is prefixHeight + (loopCount * loopHeight) + extraHeight
- For Part 1, find the height after 2022 rocks 
- For Part 2, find the height after 1 trillion rocks

DropRock:
- Get the current rock to be dropped from the rockIdx
- Get the rock's dimensions 
- Compute the rock's topRow = (ymin-4) - (rockHeight-1): the rock's bottom will be 3 levels 
  above the current ymin, so the subtract the rock's height -1 to get the topRow
- Start with the rock at x=2, y=topRow
- The rock is represented with its topLeft corner and its rockBounds (dimensions)
- Repeat until the rock settles:
    - Move the rock left/right depending on the current jetIdx
    - Increment the jetIdx, wrapping around if necessary
    - Check if new position has no collision: update the current top left, otherwise dont update
    - Rock falls down one level 
    - Check if new position has no collision: 
        - If no collision, update the rock position and continue with the loop 
        - If has collision going down, settle the rock at the current position by updating the grid with the rock
        - We stop the loop if we settled the rock; we also update the ymin if necessary

HasNoCollision:
- Check if rock doesn't bump into the left wall (x1 < 0)
- Check if rock doesn't bump into the right wall (x2 > WIDTH)
- Check if rock hits the floor (y2 > FLOOR)
- Check if it collides with existing rocks in the grid
- Go through each rock tile; if a # rock tile overlaps with a # grid tile, we see a collision
'''
