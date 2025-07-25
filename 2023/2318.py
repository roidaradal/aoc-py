# Advent of Code 2023 Day 18
# John Roy Daradal 

import math
from aoc import *
from shapely.geometry.polygon import Polygon

Step = tuple[delta, int, str]

def data(full: bool) -> list[Step]:
    T = {'U': U, 'D': D, 'L': L, 'R': R}
    def fn(line: str) -> Step:
        for rep in '()#': line = line.replace(rep, '')
        d, count, color = splitStr(line, None)
        return (T[d], int(count), color)
    return [fn(line) for line in readLines(23, 18, full)]

def solve() -> Solution:
    steps = data(full=True)

    # Part 1 
    total1 = computeDigArea(steps, False)

    # Part 2 
    total2 = computeDigArea(steps, True)

    return newSolution(total1, total2)

def computeDigArea(steps: list[Step], useCode: bool):
    T: dict[str, delta] = {'0': R, '1': D, '2': L, '3': U}

    curr: coords = (0,0)
    points: list[coords] = [curr]
    perimeter = 1
    for d, count, code in steps:
        if useCode:
            count = int(code[:5], 16)
            d = T[code[5]]
        perimeter += count 
        dy, dx = d 
        curr = move(curr, (dy*count, dx*count))
        points.append(curr)
    
    polygon = Polygon(points)
    area = int(polygon.area)
    perimeter = math.ceil(perimeter / 2)
    return area + perimeter

if __name__ == '__main__':
    do(solve, 23, 18)

'''
Solve:
- For Part 1, use the direction and steps from the input 
- For Part 2, get the number of steps and direction from the hexCode
    - Convert the first 5 digits of the 6-digit hexCode to decimal = number of steps 
    - 6th digit of hexCode = direction (0: R, 1: D, 2: L, 3: U)
- Go through the dig step instructions
- Increment the perimeter by the number of steps we moved in that direction
- Get the next endpoint of the polygon by moving in the direction no. of step times
- Collect the endpoints, and form the polygon using shapely.Polygon
- Get the area of the polygon, and add the ceil(perimeter/2) to get the final area
- Area only includes the left and top edge in the computation, so we add ceil(perimeter/2)
  to include the digs at the right and bottom edge
'''