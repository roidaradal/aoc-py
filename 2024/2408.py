# Advent of Code 2024 Day 08
# John Roy Daradal 

import itertools
from aoc import *

class Config: 
    def __init__(self):
        self.antenna: dict[str, list[coords]] = defaultdict(list)
        self.bounds: dims2 = (0,0)

def data(full: bool) -> Config:
    cfg = Config()
    lines = readLines(24, 8, full)
    cfg.bounds = getBounds(lines)
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == '.': continue 
            cfg.antenna[char].append((row,col))
    return cfg

def solve() -> Solution:
    cfg = data(full=True)

    # Part 1
    count1 = countAntiNodes(cfg, False)

    # Part 2
    count2 = countAntiNodes(cfg, True)

    return newSolution(count1, count2)

def countAntiNodes(cfg: Config, extend: bool) -> int:
    anti: set[coords] = set()
    for positions in cfg.antenna.values():
        for c1, c2 in itertools.combinations(positions, 2):
            (y1,x1), (y2,x2) = c1, c2 
            d1 = (y1-y2, x1-x2)
            d2 = (y2-y1, x2-x1)
            a1, a2 = c1, c2 
            for a,d in zip((a1,a2), (d1,d2)):
                while True:
                    a = move(a, d)
                    if not insideBounds(a, cfg.bounds): break 
                    anti.add(a)
                    if not extend: break
    if extend:
        for positions in cfg.antenna.values():
            anti = anti.union(set(positions))

    return len(anti)

if __name__ == '__main__':
    do(solve, 24, 8)

'''
CountAntiNodes:
- Group antenna positions based on their characters 
- For each position group, check all pair combinations 
- The delta1 will be applied to position 1 to take the positions behind it (forming a line)
- The delta2 will be applied to position 2 to take the positions after it (forming a line)
- Dont include positions if out of bounds from the grid
- For Part 1, only check the possible antinode behind pairs, don't extend
- For Part 2, extend checking of antinodes until edge of the grid; also include the antenna positions as antinode positions
'''