# Advent of Code 2021 Day 22
# John Roy Daradal 

from aoc import *

Cube = tuple[int2, int2, int2]
Command = tuple[bool, Cube]

def data(full: bool) -> list[Command]:
    def fn(line: str) -> Command:
        for rep in ('x=', 'y=', 'z='):
            line = line.replace(rep, '')
        head, tail = splitStr(line, None)
        ranges: list[int2] = []
        for part in splitStr(tail, ','):
            ranges.append(toInt2(part, '..'))
        flag = head == 'on'
        cube = (ranges[0], ranges[1], ranges[2])
        return (flag, cube)
    
    return [fn(line) for line in readLines(21, 22, full)]

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    commands = data(full=True)
    minLimit, maxLimit = -50, 50
    cubeGrid: dict[int3, bool] = defaultdict(bool)
    for flag, cube in commands:
        (xstart,xend),(ystart,yend),(zstart,zend) = cube 
        x1, x2 = max(xstart, minLimit), min(xend, maxLimit)
        y1, y2 = max(ystart, minLimit), min(yend, maxLimit)
        z1, z2 = max(zstart, minLimit), min(zend, maxLimit)
        for x in range(x1,x2+1):
            for y in range(y1,y2+1):
                for z in range(z1,z2+1):
                    cubeGrid[(x,y,z)] = flag
    return sum(cubeGrid.values())

def part2() -> int:
    commands = data(full=True)
    cubes: dict[Cube, int] = defaultdict(int)
    
    for isOn, ncube in commands:
        adjust: dict[Cube, int] = defaultdict(int)
        for ocube, sign in cubes.items():
            if sign == 0: continue # skip if 0 count
            overlap = getCubeOverlap(ocube, ncube)
            if overlap != None:
                # apply opposite sign to adjust for double counting
                adjust[overlap] += -sign
        for cube, adj in adjust.items():
            cubes[cube] += adj
        if isOn:
            cubes[ncube] += 1

    total = 0
    for cube, factor in cubes.items():
        total += cubeVolume(cube) * factor
    return total

def getCubeOverlap(cube1: Cube, cube2: Cube) -> Cube|None:
    xrange1, yrange1, zrange1 = cube1 
    xrange2, yrange2, zrange2 = cube2 
    xoverlap = getOverlap(xrange1, xrange2)
    yoverlap = getOverlap(yrange1, yrange2)
    zoverlap = getOverlap(zrange1, zrange2)
    if xoverlap != None and yoverlap != None and zoverlap != None:
        return (xoverlap, yoverlap, zoverlap)
    else:
        return None

def getOverlap(range1: int2, range2: int2) -> int2|None:
    range1, range2 = sorted([range1, range2])
    start1, end1 = range1 
    start2, end2 = range2 
    if start2 <= end1:
        return (start2, min(end1, end2))
    else:
        return None

def cubeVolume(cube: Cube) -> int:
    (x1,x2), (y1,y2), (z1,z2) = cube 
    return ((x2-x1)+1) * ((y2-y1)+1) * ((z2-z1)+1)

if __name__ == '__main__':
    do(solve, 21, 22)

'''
Part1:
- Use a defaultdict(bool) so that all cubes default to False (off)
- For each cube range, clip the x,y,z ranges to -50 to 50
- Go through all (x,y,z) cubes in the combination of x-range, y-range, and z-range
- Set that (x,y,z) cube to the on/off flag of the command 
- Count the number of on cubes in the grid 

Part2:
- For each cube to be turned on/off from the commands, check for intersections with existing cubes
- If the old cube (existing) and new cube (current) have overlap, we must correct for double-counting 
  by adding the overlap cube but with the opposite sign of the existing (to cancel out the counts)
    - Two cubes overlap if they overlap in all 3 axis: x,y,z
    - Two ranges overlap if, assuming range1 and range2 are sorted, range2 starts before/during range 1 ends
    - The intersection of two cubes is (xoverlap, yoverlap, zoverlap)
- If the flag is on, increment the count for this cube 
- Update the counts of the adjustment cubes; this makes the counts of the cube be 0, 1, or -1
- Finally, compute the volume of each cube and multiply by their factor (0, 1, or -1)
    - Volume of a cube is the product of (d2-d1)+1 for d=x,y,z
- This final volume is the number of on cubes
'''