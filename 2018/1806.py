# Advent of Code 2018 Day 06
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[coords]:
    def fn(line: str) -> coords:
        x,y = toInt2(line, ',')
        return y,x
    return [fn(line) for line in readLines(18, 6, full)]

def part1():
    points = data(full=True)
    rows = max(c[0] for c in points) + 1
    cols = max(c[1] for c in points) + 1
    count = {i:1 for i in range(len(points))}
    edge = set()
    for row in range(rows):
        for col in range(cols):
            if (row,col) in points: continue
            idx = closest((row,col), points)
            if idx != None:
                count[idx] += 1
                if row == 0 or col == 0 or row == rows-1 or col == cols-1:
                    edge.add(idx)
    counts = [(x,i) for i,x in count.items() if i not in edge]
    maxArea = max(counts)[0]
    print(maxArea)


def part2():
    points = data(full=True) 
    rows = max(c[0] for c in points) + 1
    cols = max(c[1] for c in points) + 1
    goal = 10_000
    fn = lambda c: sum(manhattan(c, pt) for pt in points) < goal
    cells = [(row,col) for row in range(rows) for col in range(cols)]
    count = countValid(cells, fn)
    print(count)

def closest(c: coords, points: list[coords]) -> int|None:
    d = {}
    for i,pt in enumerate(points):
        d[i] = manhattan(c, pt)
    dist = [(x,i) for i,x in d.items()]
    minDist = min(dist)[0]
    indexes = [i for x,i in dist if x == minDist]
    return indexes[0] if len(indexes) == 1 else None

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Setup the grid size by finding the max row and col from the points
- For each grid cell that is not a point, find the point closest to it
- Keep track of the number of cells closest to each point
- If there is more than 1 closest point, it doesnt belong to anyone
- Keep track of points that reach the edges of the grid (exclude because infinite)
- Get the point with maximum count that is not on the edge

Part2:
- Setup the grid size similar to Part 1
- Go through the grid cells (rows, cols)
- Count cells where sum of manhattan distances from cell to all points < 10_000
'''