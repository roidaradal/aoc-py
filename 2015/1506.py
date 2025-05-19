# Advent of Code 2015 Day 06
# John Roy Daradal 

from aoc import *

command = tuple[int,int,int,int,int] # (1/0/-1), y1, x1, y2, x2 
on, off, toggle = 'turn on', 'turn off', 'toggle'

def data(mask: dict[str,int], full: bool) -> list[command]:
    def fn(line: str) -> command:
        b = 0
        if line.startswith(on):
            b = mask[on]
        elif line.startswith(off):
            b = mask[off]
        elif line.startswith(toggle):
            b = mask[toggle]
        head,c2 = splitStr(line, 'through')
        c1 = splitStr(head,None)[-1]
        x1,y1 = toIntList(c1, ',')
        x2,y2 = toIntList(c2, ',')
        return (b, y1, x1, y2+1, x2+1)
    return [fn(line) for line in readLines(15, 6, full)]

def part1():
    mask = {on: 1, off: 0, toggle: -1}
    commands = data(mask, full=True)
    side = 1000
    grid = {(y,x): False for y in range(side) for x in range(side)}
    for b,y1,x1,y2,x2 in commands:
        for y in range(y1,y2):
            for x in range(x1,x2):
                pt = (y,x)
                if b == -1:
                    grid[pt] = not grid[pt]
                else:
                    grid[pt] = bool(b)
    print(sum(grid.values()))

def part2():
    mask = {on: 1, off: -1, toggle: 2}
    commands = data(mask, full=True)
    side = 1000 
    grid = {(y,x): 0 for y in range(side) for x in range(side)}
    for b,y1,x1,y2,x2 in commands:
        for y in range(y1,y2): 
            for x in range(x1,x2):
                pt = (y,x)
                value = grid[pt] + b 
                grid[pt] = max(value, 0)
    print(sum(grid.values()))

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Mask: {on: 1, off: 0, toggle: flip}
- Initialize grid of 1000x1000 lights to all off (False)
- Process commands: from y1 to y2 and x1 to x2, update grid light based on flag 
- If toggle, flip the light state; else, set to the on/off 
- Sum up the grid values to get the count of turned on lights

Part2:
- Mask: {on: increase 1, off: decrease 1, toggle: increase 2}
- Initialize grid of 1000x1000 lights to brightness = 0 
- Process commands: from y1 to y2 and x1 to x2, similar to Part 1 
- Add the brightness adjustment value to current grid brightness (capped at 0, cannot be negative)
- Sum up grid values to get total brightness of grid
'''