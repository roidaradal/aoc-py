# Advent of Code 2018 Day 01
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int]:
    return [int(line) for line in readLines(18, 1, full)]

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    numbers = data(full=True)
    fn = lambda x: x 
    return getTotal(numbers, fn)

def part2() -> int:
    changes = data(full=True)
    limit = len(changes)
    done = set()
    i, curr = 0, 0
    while True:
        curr += changes[i]
        if curr in done:
            break
        done.add(curr)
        i = (i+1) % limit 
    return curr

if __name__ == '__main__':
    do(solve, 18, 1)

'''
Part1:
- Sum up the numbers from the input

Part2:
- Loop through the changes (with wraparound)
- Find first value that is reached twice
'''