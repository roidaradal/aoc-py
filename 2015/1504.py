# Advent of Code 2015 Day 04
# John Roy Daradal 

from aoc import * 

def data(full: bool) -> str:
    return readLines(15, 4, full)[0]

def part1():
    key = data(full=True)
    solve(key, 5)

def part2():
    key = data(full=True)
    solve(key, 6)

def solve(key: str, numZeros: int):
    goal = '0' * numZeros 
    hashGen = md5HashGenerator(key, goal, 1)
    i,_ = next(hashGen)
    print(i)

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Solve:
- Combine key + i and get md5 hash 
- If hash starts with N zeros, output i's value
- Else, Increment i and repeat until goal found
'''