# Advent of Code 2022 Day 01
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int]:
    calories = []
    curr = 0
    for line in readLines(22, 1, full):
        if line == '':
            calories.append(curr)
            curr = 0
        else:
            curr += int(line)
    calories.append(curr)
    return calories

def solve() -> Solution:
    calories = data(full=True)

    # Part 1
    maxCal = max(calories)

    # Part 2 
    calories.sort(reverse=True)
    top3 = sum(calories[0:3])

    return newSolution(maxCal, top3)

if __name__ == '__main__':
    do(solve, 22, 1)

'''
TopCalories:
- In processing data, sum up the calories of each elf
- For Part 1, simply return the max calorie value 
- For Part 2, sort the calories in descending order and get the sum of the top 3
'''