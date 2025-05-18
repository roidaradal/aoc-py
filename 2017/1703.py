# Advent of Code 2017 Day 03
# John Roy Daradal 

import math
from aoc import * 

def data(full: bool) -> int:
    line = readLines(17, 3, full)[0]
    return int(line)

def part1():
    x = data(full=True)
    c = spiralCoords(x)
    print(manhattan(c)) 

def part2():
    goal = data(full=True)
    spiral: dict[coords,int] = {(0,0) : 1}
    values = [0, 1] 
    x, value = 2, 0 
    while value <= goal:
        curr = spiralCoords(x)
        near = [c for c in surround8(curr) if c in spiral]
        value = sum(values[spiral[c]] for c in near)
        values.append(value)
        spiral[curr] = x 
        x +=1 
    print(value)

def spiralLayer(x: int) -> int:
    dims = math.ceil(math.sqrt(x))
    if dims % 2 == 0: dims += 1 
    return (dims-1) // 2

def spiralOffset(x: int, layer: int) -> strInt:
    if layer == 0: return ('C', 0)
    side = 'BLTR' # Corner ranges go from B -> L -> T -> R
    corners = spiralCorners(layer) 
    for i in range(len(corners)-1):
        c2, c1 = corners[i], corners[i+1]
        if not (c2 >= x >= c1): continue 
        
        mid = (c1 + c2) // 2 
        offset = (x - mid) if i < 2 else (mid - x)
        return (side[i], offset)
    return ('C',0)

def spiralCorners(layer: int) -> list[int]:
    if layer == 0: return [] # no corners on layer 0 
    dims = (layer*2) + 1 
    step = dims-1 
    corners = [dims**2]
    for i in range(4):
        corners.append(corners[i] - step)
    return corners

def spiralCoords(x: int) -> coords:
    layer = spiralLayer(x)
    side, offset = spiralOffset(x, layer)
    factor = 1 if side in 'BR' else -1 
    layer *= factor
    if side == 'T' or side == 'B':
        return (layer, offset)
    else:
        return (offset, layer)

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Compute the spiralCoords of x 
- Compute the manhattan distance

Part2:
- Keep track of coords => x mapping 
- Collect computed values in a list 
- Increment x while value is not greater than goal value:
    - Compute current x's spiralCoords
    - Get the 8 surrounding coords, keep only those that are already in spiral 
    - value = sum of values of nearby coords (lookup values from list)
    - Add value to list, and the new coords => x mapping to the spiral
    
SpiralLayer:
- Spiral boxes go 1x1, 3x3, 5x5, 7x7, ... 
- Pattern: Odd length sides
    - Layer 0:  1 
    - Layer 1:  2-9 
    - Layer 2:  10-25 
    - Layer 3:  26-49
- To get sideLength of layer of x, get the ceil(sqrt(x)):
    - Example: 24 => ceil(sqrt(24)) = 5 
    - Example: 4 => ceil(sqrt(4)) = 2 
- No even sideLengths, so if even, add 1 to go to next odd sideLength 
- To get the layer number (index in the odd number sequence): (dims-1) / 2
    - 1     0/2     0
    - 3     2/2     1
    - 5     4/2     2
    - 7     6/2     3

SpiralOffset:
- Get corners of current layer (descending numbers that form corners of layer square)
- Go through each corner range in order, find where x falls in range 
- Compute mid: (c1+c2)/2, need to compute offset based on mid 
- Return x - mid (for B,L), otherwise mid - x (for T,R)
- Also return corresponding side where x was found (BLTR)

SpiralCorners:
- To get sideLength of layer, reverse process above: (layer*2) + 1
- Start from sideLength^2 (last number in the layer), bottom-right corner 
- Step size = sideLength-1 
    - e.g. sideLength = 3, step = 2 => 9, 7, 5, 3, 1 
    - e.g. sideLength = 5, step = 4 => 25, 21, 17, 13, 9
- Include the lastNumber of previous layer as last corner to act as sentinel for range comparisons

SpiralCoords:
- Get layer, side and offset of x 
- If side is T or L, use -layer 
- If side is T or B, row = layer, col = offset 
- If side is L or R, row = offset, col = layer
'''