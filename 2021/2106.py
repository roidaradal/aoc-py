# Advent of Code 2021 Day 06
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int]:
    line = readFirstLine(21, 6, full)
    return toIntList(line, ',')

def solve() -> Solution:
    fish = data(full=True)

    # Part 1
    count1 = simulate(fish, 80)

    # Part 2 
    count2 = simulate(fish, 256)

    return newSolution(count1, count2)

def simulate(fish: list[int], days: int) -> int:
    groups = defaultdict(int)
    for x in fish:
        groups[x] += 1 
    
    for _ in range(days):
        groups2 = defaultdict(int)
        for timer, count in groups.items():
            if timer == 0:
                timer = 6 
                groups2[8] = count 
            else:
                timer -= 1
            groups2[timer] += count 
        groups = groups2 
    return sum(groups.values())

if __name__ == '__main__':
    do(solve, 21, 6)

'''
Simulate:
- For Part 1, run for 80 days; for Part 2, run for 256 days 
- Group the fish by their timer: this ensures we are only doing at most 7 computations each day 
- Repeat the process for the given number of days 
- Decrement the fish group's timer in each day 
- If timer reaches 0, timer for the group resets to 6, but it also adds new fish (equal to number of parents) with timer=8
- Total fish after number of days is the sum of group's counts
'''