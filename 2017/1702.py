# Advent of Code 2017 Day 02
# John Roy Daradal 

import itertools
from aoc import * 

def data(full: bool) -> list[list[int]]:
    fn = lambda line: toIntList(line, None)
    return [fn(line) for line in readLines(17, 2, full)]

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    numbersList = data(full=True) 
    fn = lambda numbers: max(numbers) - min(numbers) 
    return getTotal(numbersList, fn)

def part2() -> int:
    numbersList = data(full=True) 
    def fn(numbers: list[int]) -> int:
        for pair in itertools.combinations(numbers, 2):
            a, b = sorted(pair)
            if b % a == 0:
                return b // a 
        return 0
    return getTotal(numbersList, fn)

if __name__ == '__main__':
    do(solve, 17, 2)

'''
Part1:
- Compute total going through each numbers list 
- Get difference between max(numbers) and min(numbers)

Part2:
- Compute total going through each numbers list 
- Find pair of numbers where b cleanly divides a
- Sum up the quotients of b / a of valid pairs
'''