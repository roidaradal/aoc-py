# Advent of Code 2022 Day 06
# John Roy Daradal 

from aoc import *

def data(full: bool) -> str:
    return readLines(22, 6, full)[0]

def part1():
    line = data(full=True)
    marker = findMarker(line, 4)
    print(marker) 

def part2():
    line = data(full=True)
    marker = findMarker(line, 14)
    print(marker) 

def findMarker(line: str, length: int) -> int:
    for n in range(length, len(line)+1):
        if allUnique(line[n-length:n]):
            return n 
    return -1

def allUnique(text: str) -> bool:
    return len(text) == len(set(text))

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
FindMarker:
- Check N-length substrings from the given word 
- If all characters are unique in that substring, return that index
- For Part 1, find markers of size 4; for Part find markers of size 14
'''