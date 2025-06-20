# Advent of Code 2022 Day 06
# John Roy Daradal 

from aoc import *

def data(full: bool) -> str:
    return readFirstLine(22, 6, full)

def solve() -> Solution:
    line = data(full=True)

    # Part 1
    marker1 = findMarker(line, 4)

    # Part 2 
    marker2 = findMarker(line, 14)

    return newSolution(marker1, marker2)

def findMarker(line: str, length: int) -> int:
    for n in range(length, len(line)+1):
        if allUnique(line[n-length:n]):
            return n 
    return -1

def allUnique(text: str) -> bool:
    return len(text) == len(set(text))

if __name__ == '__main__':
    do(solve, 22, 6)

'''
FindMarker:
- Check N-length substrings from the given word 
- If all characters are unique in that substring, return that index
- For Part 1, find markers of size 4; for Part find markers of size 14
'''