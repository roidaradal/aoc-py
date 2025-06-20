# Advent of Code 2017 Day 05
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int]:
    return [int(line) for line in readLines(17, 5, full)]

def solve() -> Solution:
    # Part 1
    jumps = data(full=True)
    count1 = countJumps(jumps, False)

    # Part 2
    jumps = data(full=True)
    count2 = countJumps(jumps, True)

    return newSolution(count1, count2)

def countJumps(jumps: list[int], clip: bool) -> int: 
    limit = len(jumps)
    i, count = 0, 0 
    while 0 <= i < limit: 
        jump = jumps[i]
        increment = 1 
        if clip and jump >= 3:
            increment = -1
        jumps[i] += increment
        i += jump 
        count += 1
    return count


if __name__ == '__main__':
    do(solve, 17, 5)

'''
Solve:
- Count jump steps until index goes out of bounds 
- Increment index by current jump value
- For part 1: always increment by 1 
- For part 2: if current value >= 3, decrease by 1, else increase by 1
'''