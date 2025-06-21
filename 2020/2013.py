# Advent of Code 2020 Day 13
# John Roy Daradal 

import math
from aoc import *

Bus = tuple[int, int] # offset, busID

def data(full: bool) -> tuple[int, list[Bus]]:
    lines = readLines(20, 13, full)
    line1, line2 = lines 
    start = int(line1)
    buses = [(i, int(x)) for i,x in enumerate(splitStr(line2, ',')) if x.isdigit()]
    return start, buses 

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    start, buses = data(full=True)
    busStart: list[int2] = []
    for _, bus in buses:
        loops = math.ceil(start / bus)
        busStart.append((bus * loops, bus))
    earliest, bus = min(busStart)
    wait = earliest - start 
    return wait * bus
    
def part2() -> int:
    _, buses = data(full=True)
    t = 0 
    skip = 1 
    for offset, bus in buses:
        while True:
            t += skip # skip time by current skip (accumulates and grows after each processed bus)
            if (t + offset) % bus == 0: # found a clean division with time+offset, stop loop 
                skip = skip * bus # increase the skip by current bus ID
                break
    return t

if __name__ == '__main__':
    do(solve, 20, 13)

'''
Part1:
- StartTime = earliest time you can depart
- For each bus, compute the minimum time it departs that is greater than the earliest time you can depart
- Get the bus that gives you minimum time to wait = the earliest time 
- Return the amount of wait time (departure - startTime) * busID 

Part2:
- Find the earliest time where buses depart at offsets matching their position on the list 
- Idea: accumulate the time skip while going through buses, baking into the skip value that it is a factor of the previous buses
    - For bus 1, only has to find a clean division for itself; once found, skip = bus1 
    - For bus 2, has to find a clean division with current time + offset (index)
    - Once we find it, update the skip = bus1 * bus2
    - For bus 3, has to find clean division with time + offset, skipping by bus1*bus2
    - Once we find it, the skip is now = bus1 * bus2 * bus3
- Note: this works because the numbers are all prime
- Return the timestamp after processing all buses
'''