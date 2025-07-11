# Advent of Code 2021 Day 17
# John Roy Daradal 

from aoc import *

def data(full: bool) -> tuple[int2, int2]:
    line = readFirstLine(21, 17, full)
    line = splitStr(line, ':')[1]
    for rep in ('x=', 'y='): line = line.replace(rep, '')
    x, y = splitStr(line, ',')
    xrange = toInt2(x, '..')
    yrange = toInt2(y, '..')
    return yrange, xrange

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    targetArea = data(full=True)
    (ymin, ymax), (xmin, xmax) = targetArea
    limit = max(abs(x) for x in (ymin, ymax, xmin, xmax))
    start, end = 1, limit+1
    maxPeak = 0
    for dy in range(1, limit+1):
        start2, count = 0, 0
        for dx in range(start, end):
            path, landed = launchProbe(targetArea, (dy, dx))
            peak = max(c[0] for c in path) if landed else 0
            maxPeak = max(maxPeak, peak)
            if landed:
                if start2 == 0: start2 = dx
                count += 1
        if count > 0:
            start, end = start2, start2 + count 
    return maxPeak

def part2() -> int:
    targetArea = data(full=True)
    (ymin, ymax), (xmin, xmax) = targetArea
    limit = max(abs(x) for x in (ymin, ymax, xmin, xmax))
    count = 0
    for dy in range(ymin, limit+1):
        for dx in range(1, xmax+1):
            _, landed = launchProbe(targetArea, (dy,dx))
            if landed: count += 1
    return count

def launchProbe(targetArea: tuple[int2, int2], velocity: delta) -> tuple[list[coords], bool]:
    (ymin, ymax), (xmin, xmax) = targetArea 
    y, x = (0, 0)
    dy, dx = velocity
    path: list[coords] = [(y,x)]
    while True:
        # Move position
        y, x = y+dy, x+dx 
        path.append((y, x))
        # Adjust velocity
        if dx > 0:
            dx -= 1 
        elif dx < 0:
            dx += 1
        dy -= 1
        # Check if inside target area 
        if ymin <= y <= ymax and xmin <= x <= xmax:
            return path, True 
        # Check if already overshot target area 
        if y < ymin: 
            return path, False 

if __name__ == '__main__':
    do(solve, 21, 17)

'''
Part1:
- Extract ymin, ymax, xmin, xmax from the target area ranges
- We explore values for dy from 1 up to the maximum absolute value of ymin, ymax, xmin, or xmax
    - y cannot be 0 or negative because we are aiming for the highest peak, it has to elevate first
    - We use the maximum magnitude in any direction because more than that will surely overshoot 
- Start with the range of dx from 1 to limit, but we will shrink this range down to the x-range where 
  our launched probe reached the target area
- If any of the dx values on the current dy has reached the target area, we shrink the next dx range 
- If none of the dx values on the  current dy reached the target area, we keep the dx range untouched
- For each dx from the current range, we check if the initial velocity (dy,dx) will reach the target area
    - Start at position (0,0) and the initial velocity, keep track of the positions visited in the path
    - Move the position based on the current velocity
    - Adjust the dx by moving it closer to 0 (decrement if positive, increment if negative)
    - Adjust the dy by decrementing it
    - If the current position is inside the target area range, return path and True (landed)
    - If the position has already overshot the target area (y < ymin), we stop and return False
- The launch probe function returns the path it traveled and whether it landed on the target area or not
- If it landed, we try to update the max peak we have seen so far by getting the max y value on the path
- Output the maxPeak of the paths that landed on the target area 

Part2:
- For Part 2, we will count the number of possible initial velocities that will reach the target area
- Extract ymin, ymax, xmin, xmax from the target area ranges, similar to Part 1 
- The limit is still the maximum absolute value out of these 4 values 
- The dy range is now extended from ymin to the limit - we can now use -dy right away so that in one step
  we can reach the target area: because unlike in Part 1, we are not worried about the peak height anymore
- The dx range is now limited from 1 to xmax (cannot be 0 or negative, otherwise it will fall straight down or backwards)
- For the combinations of dy,dx in these ranges, test which initial velocities end up in the target area
- Return the count of valid initial velocities
'''