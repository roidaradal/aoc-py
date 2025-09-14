# Advent of Code 2023 Day 22
# John Roy Daradal 

from aoc import *

X_AXIS, Y_AXIS, Z_AXIS = 0, 1, 2 

class Brick:
    def __init__(self, name: int, start: int3, end: int3):
        self.name = name
        self.x1, self.y1, self.z1 = start 
        self.x2, self.y2, self.z2 = end 
        self.orientation = -1
        for i in range(3):
            if start[i] != end[i]:
                self.orientation = i 
                break 
        
        self.cubes: set[int3] = set()
        x, y, z = start 
        if self.orientation == -1:
            self.cubes.add((x, y, z))
        elif self.orientation == X_AXIS:
            for x in range(self.x1, self.x2+1):
                self.cubes.add((x, y, z))
        elif self.orientation == Y_AXIS:
            for y in range(self.y1, self.y2+1):
                self.cubes.add((x, y, z))
        elif self.orientation == Z_AXIS:
            for z in range(self.z1, self.z2+1):
                self.cubes.add((x,y,z))
    
    def goDown(self):
        self.z1 -= 1 
        self.z2 -= 1
        cubes: set[int3] = set()
        for x,y,z in self.cubes:
            cubes.add((x,y,z-1))
        self.cubes = cubes
    
    def goUp(self): 
        self.z1 += 1
        self.z2 += 1
        cubes: set[int3] = set()
        for x,y,z in self.cubes:
            cubes.add((x,y,z+1))
        self.cubes = cubes

def data(full: bool) -> list[Brick]:
    def fn(line: str, name: int) -> Brick:
        head, tail = splitStr(line, '~')
        start = toInt3(head, ',')
        last  = toInt3(tail, ',')
        return Brick(name, start, last)
    return [fn(line, i+1) for i, line in enumerate(readLines(23, 22, full))]

def solve() -> Solution:
    bricks = data(full=True)
    bricks.sort(key = lambda b: b.z1)

    # Drop bricks down
    occupied: dict[int3, int] = defaultdict(int)
    for brick in bricks:
        while True:
            if brick.z1 == 1: # reached bottom
                for cube in brick.cubes: 
                    occupied[cube] = brick.name
                break 
            brick.goDown()
            if hasCollision(brick, occupied):
                brick.goUp()
                for cube in brick.cubes: 
                    occupied[cube] = brick.name
                break
    
    # Create the support graph: brick is supported by set of supporters below
    support: dict[int, set[int]] = {brick.name : set() for brick in bricks}
    for cube, name in occupied.items():
        if name == 0: continue 
        above = cubeAbove(cube)
        if above in occupied and occupied[above] not in (0, name): # not blank or same brick
            nameAbove = occupied[above]
            support[nameAbove].add(name)
    
    # Check which bricks cannot be safely disintegrated
    disintegrate: set[int] = {brick.name for brick in bricks}
    total = 0 
    for above, supporters in support.items():
        if len(supporters) != 1: continue 
        supporter = tuple(supporters)[0]
        if supporter in disintegrate:
            # Part 1
            disintegrate.remove(supporter)
            # Part 2
            total += countAffected(support, supporter)
    count = len(disintegrate)

    return newSolution(count, total)

def hasCollision(brick: Brick, occupied: dict[int3, int]) -> bool:
    return any(occupied[cube] != 0 for cube in brick.cubes)

def cubeAbove(cube: int3) -> int3:
    x,y,z = cube 
    return (x,y,z+1)

def countAffected(support: dict[int, set[int]], brick: int) -> int:
    removed: set[int] = {brick}
    while True:
        updated = False 
        for above, supporters in support.items():
            if above in removed: continue
            if len(supporters) == 0: continue 

            left = supporters - removed 
            if len(left) == 0:
                removed.add(above)
                updated = True
        if not updated: break
    return len(removed) - 1 # don't include initial removed brick

if __name__ == '__main__':
    do(solve, 23, 22)

'''
Solve:
- Create Brick objects from the input data:
    - Find the brick's orientation: the axis where the start and end range values differ
    - If there is no such axis, then this brick consist of 1 cube only
    - Create the cubes of this brick, by going through the range of values in the orientation axis
- Sort the bricks by their z1 (lower values first = closer to the ground)j
- Drop the sorted bricks down one-by-one:
    - If the brick's z1 is 1, we have reached the bottom, so we settle the brick here
    - Keep dropping the brick down until we find a collision:
        - If we drop the brick, we also adjust the brick's z values (z1-1, z2-1, cubes: z-1)
        - There is a collision if any one of the brick's cubes are already occupied by another brick
    - If we detect a collision, bring the brick back up and settle it there
        - We're undoing the previous going down, since it resulted in a collision
        - Adjust the brick's z values (z1+1, z2+1, cubes: z+1)
    - Settling a brick = setting the brick's cube positions as occupied by this brick name
- After all the bricks have settled, we create the support graph:
    - A brick is supported by a set of supporters below it
    - For each occupied brick cube in the grid, check the above cube
    - If the above cube is occupied by another brick, this other brick is supported by the current brick
- For Part 1, count the number of bricks that can be safely disintegrated:
    - Initially, set the safe-to-disintegrate list to all bricks
    - Find bricks that are the lone supporter of another brick: these are unsafe, as removing this
      would cause the other brick to fall since there are no other supporters
    - We remove the unsafe bricks from the list, and output the final count of safe to disintegrate bricks
- For Part 2, count the total bricks that will be affected if we disintegrate an unsafe brick:
    - While removing the unsafe bricks from the list in Part 1, we also count how many bricks 
      will topple if we do decide to remove this brick (chain reaction)
    - Start with the removed set with this one brick
    - Repeat until we don't see any updates:
        - Check what will remain from the supporters of a brick, if we remove the removed set 
        - If no supporters will be left, we add this brick to the removed set (as this will fall)
    - The final count is removed-1 (don't include the initial removed brick)
    - Output the total count of affected bricks
'''