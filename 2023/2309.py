# Advent of Code 2023 Day 09
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[list[int]]:
    def fn(line: str) -> list[int]:
        return toIntList(line, None)
    return [fn(line) for line in readLines(23, 9, full)]

def solve() -> Solution:
    numberLists = data(full=True)

    # Part 1
    total1 = getTotal(numberLists, getNext)
    
    # Part 2
    total2 = getTotal(numberLists, getPrev)

    return newSolution(total1, total2)

def getNext(numbers: list[int]) -> int:
    gap = 0
    diff = numbers 
    while not all(d == 0 for d in diff):
        diff = [diff[i]-diff[i-1] for i in range(1, len(diff))]
        gap += diff[-1]
    return numbers[-1] + gap

def getPrev(numbers: list[int]) -> int:
    diff = numbers 
    fronts = [diff[0]]
    while not all(d == 0 for d in diff):
        diff = [diff[i]-diff[i-1] for i in range(1, len(diff))]
        fronts.append(diff[0])
    while len(fronts) >= 2:
        b = fronts.pop()
        a = fronts.pop()
        fronts.append(a-b)
    return fronts[0]

if __name__ == '__main__':
    do(solve, 23, 9)

'''
Part1:
- Find the next number in the input list
- Start with diff = numbers; loop until all diffs are 0
- At each iteration, compute diff by finding pairwise difference of consecutive numbers
- The gap for that round is the last number, which is what we will add to the level above it to get the next number
- After exiting the loop, add the total gap to the last number of the input list: this is the next number of that series
- Output the total next numbers of all numberLists

Part2:
- Find the previous number in the input list
- Start with diff = numbers, loop until all diffs are 0
- Compute the diffs similar to Part 1
- Instead of the last number (Part 1), keep track of the front numbers at each round 
- After exiting the loop, repeatedly get the difference of the last 2 fronts and add their difference to the end
- Stop if we only have one number in the fronts list: that is the previous number of the input list
- Output the total previous numbers of all numberLists
'''