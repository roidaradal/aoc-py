# Advent of Code 2016 Day 20
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int2]:
    def fn(line: str) -> int2:
        start, last = toInt2(line, '-')
        return (start, last+1)
    return [fn(line) for line in readLines(16, 20, full)]

def solve() -> Solution:
    blacklist = data(full=True)
    blacklist = mergeRanges(blacklist)

    # Part 1 
    _, end = blacklist[0]
    minValid = end

    # Part 2 
    count = 0
    prevEnd = end 
    for start, end in blacklist[1:]:
        count += start - prevEnd
        prevEnd = end

    return newSolution(minValid, count)

if __name__ == '__main__':
    do(solve, 16, 20)

'''
Solve:
- In reading data, convert the ranges into [start, end) ranges by adding 1 to the right bound
- Sort the ranges and merge them to simplify the processing 
- For Part 1, the minimum value not blocked is the first range's end (non-inclusive)
- For Part 2, the total number of valid values is the total of gaps between the sorted ranges
'''