# Advent of Code 2025 Day 02
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int2]:
    def fn(line: str) -> int2:
        a, b = line.split('-')
        return int(a), int(b)
    return [fn(line) for line in readFirstLine(25, 2, full).split(',')]

def solve() -> Solution:
    ranges = data(full=True)
    total1, total2 = 0, 0
    for first, last in ranges:
        for x in range(first, last+1):
            if isInvalid(x):
                total1 += x
            if isInvalid2(x):
                total2 += x
    return newSolution(total1, total2)


def isInvalid(x: int) -> bool:
    s = str(x)
    if len(s) % 2 == 0:
        half = len(s) // 2 
        return s[:half] == s[half:]
    else:
        return False # not invalid if odd length
    
def isInvalid2(x: int) -> bool:
    s = str(x)
    length = len(s)
    half = length // 2
    for w in range(1, half+1):
        if length % w != 0:
            continue # skip if not evenly divisible 
        repeat = length // w
        if s[:w] * repeat == s:
            return True
    return False

if __name__ == '__main__':
    do(solve, 25, 2)

'''
Solve:
- Go through each number listed in the ranges
- If number is invalid, add the number to the total
- For Part 1, number is invalid if length is even and left half == right half
- For Part 2, go through various widths from 1 to half length,
  if length is evenly divisible by width, check if repeating the string[:width]
  to produce the full string is the number string, if it is, it's invalid.
'''