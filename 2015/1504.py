# Advent of Code 2015 Day 04
# John Roy Daradal 

from aoc import * 

def data(full: bool) -> str:
    return readFirstLine(15, 4, full)

def solve() -> Solution:
    key = data(full=True)

    # Part 1
    idx1 = findIndex(key, 5)

    # Part 2
    idx2 = findIndex(key, 6)

    return newSolution(idx1, idx2)

def findIndex(key: str, numZeros: int) -> int:
    goal = '0' * numZeros 
    hashGen = md5HashGenerator(key, goal, 1)
    i,_ = next(hashGen)
    return i

if __name__ == '__main__':
    do(solve, 15, 4)

'''
Solve:
- Combine key + i and get md5 hash 
- If hash starts with N zeros, output i's value
- Else, Increment i and repeat until goal found
'''