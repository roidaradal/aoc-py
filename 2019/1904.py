# Advent of Code 2019 Day 04
# John Roy Daradal 

from aoc import *

def data(full: bool) -> dims2:
    line = readLines(19, 4, full)[0]
    return toDims2(line, '-')

def part1():
    start, end = data(full=True)
    numbers = list(range(start,end))
    count = countValid(numbers, isValid)
    print(count)

def part2():
    start, end = data(full=True)
    numbers = list(range(start,end))
    count = countValid(numbers, isValid2)
    print(count) 

def isValid(number: int) -> bool:
    x = str(number)
    # Check if increasing digits 
    if x != sortedStr(x): return False 
    
    # Check if has adjacent digits that are same 
    return hasTwins(x)

def isValid2(number: int) -> bool:
    x = str(number)
    # Check if increasing digits 
    if x != sortedStr(x): return False 
    
    # Check if has length 2 grouped chunk 
    sizes = set(len(chunk) for chunk in groupChunks(x))
    return 2 in sizes

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Valid password if digits are all non-decreasing (must be in sorted order)
- Check if has adjacent digits that are the same

Part2:
- Also needs to have non-decreasing digits 
- Group chunks of digits, ensure there is a chunk of size 2
'''