# Advent of Code 2017 Day 05
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int]:
    return [int(line) for line in readLines(17, 5, full)]

def part1():
    jumps = data(full=True)
    increment = lambda jump: 1 
    count = countJumps(jumps, increment)
    print(count)

def part2():
    jumps = data(full=True)
    increment = lambda jump: -1 if jump >= 3 else 1
    count = countJumps(jumps, increment)
    print(count) 

def countJumps(jumps: list[int], increment: Callable) -> int: 
    limit = len(jumps)
    i, count = 0, 0 
    while 0 <= i < limit: 
        jump = jumps[i]
        jumps[i] += increment(jump)
        i += jump 
        count += 1
    return count


if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Solve:
- Count jump steps until index goes out of bounds 
- Increment index by current jump value
- For part 1: always increment by 1 
- For part 2: if current value >= 3, decrease by 1, else increase by 1
'''