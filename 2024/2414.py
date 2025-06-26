# Advent of Code 2024 Day 14
# John Roy Daradal 

from aoc import *

Robot = tuple[coords, delta]

def data(full: bool) -> list[Robot]:
    def fn(line: str) -> Robot:
        for remove in ['p=', 'v=']: line = line.replace(remove, '')
        p, v = splitStr(line, None)
        px, py = toInt2(p, ',')
        vx, vy = toInt2(v, ',')
        return (py,px), (vy,vx)
    return [fn(line) for line in readLines(24, 14, full)]

def solve() -> Solution:
    bounds: dims2 = (103,101)

    # Part 1
    robots = data(full=True)
    for _ in range(100):
        moveRobots(robots, bounds)
    factor = safetyFactor(robots, bounds)

    # Part 2
    robots = data(full=True)
    scores: list[int2] = []
    cache: dict[int, list[coords]] = {}
    for s in range(10_000):
        moveRobots(robots, bounds)
        scores.append((safetyFactor(robots, bounds), s+1))
        cache[s+1] = [c for c,_ in robots]
    _, seconds = min(scores)
    # displayGrid(cache[seconds], bounds)

    return newSolution(factor, seconds)

def moveRobots(robots: list[Robot], bounds: dims2):
    rows, cols = bounds 
    for i, (c,d) in enumerate(robots):
        y,x = move(c, d)
        if y < 0:
            y = rows + y 
        elif y >= rows:
            y = y % rows 
        if x < 0:
            x = cols + x 
        elif x >= cols:
            x = x % cols 
        robots[i] = ((y,x), d)

def safetyFactor(robots: list[Robot], bounds: dims2) -> int:
    rows, cols = bounds 
    count: dict[coords, int] = defaultdict(int)
    for c,_ in robots:
        count[c] += 1

    q1, q2, q3, q4 = 0, 0, 0, 0 
    midRow, midCol = rows // 2, cols // 2 
    for row in range(0, midRow):
        for col in range(cols):
            pt = (row, col)
            if pt not in count: continue 
            if col < midCol:
                q1 += count[pt]
            elif col > midCol:
                q2 += count[pt]
    for row in range(midRow+1, rows):
        for col in range(cols):
            pt = (row, col)
            if pt not in count: continue 
            if col < midCol:
                q3 += count[pt]
            elif col > midCol:
                q4 += count[pt]
    return q1 * q2 * q3 * q4

def displayGrid(positions: list[coords], bounds: dims2):
    rows, cols = bounds 
    grid = [['.' for _ in range(cols)] for _ in range(rows)]
    for row,col in positions:
        grid[row][col] = '#'
    for line in grid: print(''.join(line))


if __name__ == '__main__':
    do(solve, 24, 14)

'''
Solve:
- For Part 1, move the robots for 100 steps and output the safety factor after 
- For Part 2, move the robots for 10,000 steps, remembering the safety factor and robot positions each second 
- Find the time with the minimum safety factor = this is when the Christmas Tree is displayed
- Idea: this is when the points are mostly concentrated more on one quadrant 
- To move a robot, apply its delta to the current position; wrap-around to the front or back if exceeds bounds
- To compute the robot positions' safety factor, first count the number of robots present for each grid cell
- Then count the number of robots in q1, q2, q3, q4 by dividing the rows and columns across the middle 
- The safety factor is the product of the total counts of the 4 quadrants
'''