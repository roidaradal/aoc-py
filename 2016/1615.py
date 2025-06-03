# Advent of Code 2016 Day 15
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int2]:
    def fn(line: str) -> int2:
        p = line.strip('.').split()
        count, start = int(p[3]), int(p[-1])
        return count, start
    return [fn(line) for line in readLines(16, 15, full)]

def solve():
    discs = data(full=True) 
    t = findPressTime(discs)
    print(t)
    
    discs.append((11, 0))
    t = findPressTime(discs)
    print(t)

def findPressTime(discs: list[int2]) -> int:
    t = 0
    while True:
        pos = positions(discs, t)
        if all(p == 0 for p in pos):
            return t 
        t += 1

def positions(discs: list[int2], t: int) -> list[int]:
    pos = []
    for i,(count,start) in enumerate(discs):
        moves = t + i + 1 
        end = (start + moves) % count 
        pos.append(end)
    return pos 

if __name__ == '__main__':
    do(solve)

'''
Solve:
- Find the time at which all predicted disc positions align at position 0, incrementing time from 0
- To find the position of discs at a given time t, 
    - Move the disc t times (for the time passed)
    - Also move the disc i+1 times, where i is the disc index, because the first disc moves at 1s, then
      the second disc would have moved two times by the time the ball reaches it
    - Wrap-around by the count
- Check if all predicted positions will be 0 - allows the ball to pass through
- For Part 2, add a new disc with count=11, start=0, and findPressTime
'''