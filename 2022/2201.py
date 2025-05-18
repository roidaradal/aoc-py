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

def part1():
    calories = data(full=True)
    print(max(calories)) 

def part2():
    calories = data(full=True)
    calories.sort(reverse=True)
    top3 = sum(calories[0:3])
    print(top3) 

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
TopCalories:
- In processing data, sum up the calories of each elf
- For Part 1, simply return the max calorie value 
- For Part 2, sort the calories in descending order and get the sum of the top 3
'''