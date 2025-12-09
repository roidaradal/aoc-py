# Advent of Code 2025 Day 09
# John Roy Daradal 

import itertools
from aoc import *
from shapely.geometry.polygon import Polygon

def data(full: bool) -> list[int2]:
    return [toInt2(line,',') for line in readLines(25, 9, full)]

def solve() -> Solution:
    points = data(full=True)
    polygon = Polygon(points)
    maxArea1, maxArea2 = 0, 0 
    for p1, p2 in itertools.combinations(points, 2):
        (x1, y1), (x2, y2) = p1, p2 
        area = (abs(y1-y2)+1) * (abs(x1-x2)+1)
        maxArea1 = max(maxArea1, area)
        if polygon.contains(Polygon([p1, (x2,y1), p2, (x1, y2)])):
            maxArea2 = max(maxArea2, area)
    return newSolution(maxArea1, maxArea2)

if __name__ == '__main__':
    do(solve, 25, 9)

'''
Solve:
- Create a polygon from the points using shapely package
- Go through the combination of points
- Compute the area of the rectangle formed by the two points in opposite corners
- For Part 1, output the maximum area from the pairs
- For Part 2, only consider pairs whose rectangle is totally inside the outer polygon
  (to make sure that everything inside is red or green)
'''