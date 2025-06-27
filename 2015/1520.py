# Advent of Code 2015 Day 20
# John Roy Daradal 

from aoc import *

def data(full: bool) -> int:
    return int(readFirstLine(15, 20, full))

def solve() -> Solution:
    goal = data(full=True)

    # Part 1
    house1 = findMinHouse(goal, 10, 0)

    # Part 2 
    house2 = findMinHouse(goal, 11, 50)

    return newSolution(house1, house2)

def findMinHouse(goal: int, capacity: int, maxCount: int) -> int:
    N = goal // capacity 
    house = [0] * N 
    elf = 0
    for elf in range(1, N):
        count = 0
        for h in range(elf, N, elf):
            house[h] += elf * capacity
            count += 1 
            if maxCount > 0 and count == maxCount: break
            
    return min(h for h,total in enumerate(house) if total >= goal)



if __name__ == '__main__':
    do(solve, 15, 20)

'''
Solve: 
- For Part 1, find the minimum house that gets at least the goal value, for elf capacity = 10, and no elf visit limit 
- For Part 2, do the same, but for elf capacity = 11, and each elf only visits 50 houses
- The number of elfs we need is N = goal // capacity, because the last elf can reach the goal after 1 visit 
- Initialize houses from 0 to N with 0 
- Go through each elf from 1 to N; count the number of times the elf has visited a house (for Part 2)
- The houses elf X visits are X, 2X, 3X, 4X, etc., so go through the range elf to N, with skip=elf 
- Elf X delivers X*capacity presents to a house, so we increment the total of each house it visits 
- Stop early if we have a maxCount for the elves and it has been reached 
- Return the minimum house number whose total is at least the goal number
'''