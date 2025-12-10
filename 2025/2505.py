# Advent of Code 2025 Day 05
# John Roy Daradal 

from aoc import *

def data(full: bool) -> tuple[list[int2], list[int]]:
    ranges: list[int2] = []
    ingredients: list[int] = []
    inPart2 = False
    for line in readLines(25, 5, full):
        if line == '':
            inPart2 = True 
        elif inPart2:
            ingredients.append(int(line))
        else:
            ranges.append(toInt2(line, '-'))
    return ranges, ingredients

def solve() -> Solution:
    ranges, ingredients = data(full=True)
    ranges = mergeRanges(ranges)

    # Part 1
    count1 = sum(any(first <= i <= last for first,last in ranges) for i in ingredients)

    # Part 2
    count2 = sum(last-first+1 for first,last in ranges)
      
    return newSolution(count1, count2)

if __name__ == '__main__':
    do(solve, 25, 5)

'''
Part1:
- Go through each ingredient 
- Check if any of the ranges allows the ingredient to be in range
- Output the count of ingredients that fall in one of the ranges

Part2:
- Merge the ranges to eliminate subsets and overlaps 
- Sum up the sizes of the resulting ranges
'''