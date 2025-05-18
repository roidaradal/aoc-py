# Advent of Code 2018 Day 01
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int]:
    return [int(line) for line in readLines(18, 1, full)]

def part1():
    numbers = data(full=True)
    fn = lambda x: x 
    total = getTotal(numbers, fn)
    print(total) 

def part2():
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
    print(curr)

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Sum up the numbers from the input

Part2:
- Loop through the changes (with wraparound)
- Find first value that is reached twice
'''