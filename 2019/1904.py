# Advent of Code 2019 Day 04
# John Roy Daradal 

from aoc import *

def data(full: bool) -> dims2:
    line = readFirstLine(19, 4, full)
    return toDims2(line, '-')

def solve() -> Solution:
    start, end = data(full=True)
    numbers = list(range(start,end))

    # Part 1
    count1 = countValid(numbers, isValid)

    # Part 2
    count2 = countValid(numbers, isValid2)
    
    return newSolution(count1, count2) 

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
    do(solve, 19, 4)

'''
Part1:
- Valid password if digits are all non-decreasing (must be in sorted order)
- Check if has adjacent digits that are the same

Part2:
- Also needs to have non-decreasing digits 
- Group chunks of digits, ensure there is a chunk of size 2
'''