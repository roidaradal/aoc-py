# Advent of Code 2017 Day 17
# John Roy Daradal 

from aoc import *

def data(full: bool) -> int:
    return int(readFirstLine(17, 17, full))

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    step = data(full=True)
    limit = 2017

    numbers = [0]
    curr = 0
    for x in range(1, limit+1):
        nxt = (curr + step) % x 
        numbers.insert(nxt+1, x)
        curr = nxt+1
    return numbers[curr+1]

def part2() -> int:
    step = data(full=True)
    limit = 50_000_000
    curr = 0
    out  = 0
    for x in range(1, limit+1):
        curr = (curr + step) % x 
        if curr == 0:
            out = x 
        curr += 1
    return out

if __name__ == '__main__':
    do(solve, 17, 17)

'''
Part1:
- Start with 0 in the numbers list, keep track of current index = 0
- Repeat from 1 to 2017:
- Next insert index is current index + step with wrap-around 
- Insert the number at that position, and move the current index forward
- Output the number after the current index after exiting the loop

Part2:
- Run the loop 50M times; no need to keep track of numbers array as 
  we only need to know the number after 0 when the loop exits
- Keep track of current index (simulated) and last known digit after 0
- The next index is computed similart to part 1 : (current + step) % x
- If the current index is 0, it will be inserting after the 0 number, 
  so update the output digit to the current number being inserted
- Step the current index forward
- In this simulation we keep 0 at the front: we don't insert before 0, 
  instead we add at the back of the list (since it is circular anyway)
'''