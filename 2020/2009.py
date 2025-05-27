# Advent of Code 2020 Day 09
# John Roy Daradal 

import itertools
from aoc import *

def data(full: bool) -> list[int]:
    return [int(line) for line in readLines(20, 9, full)]

def solve():
    numbers = data(full=True)
    limit = len(numbers)
    
    # Part 1
    window = 25
    target = 0
    for i in range(window, limit):
        if not hasPairSum(numbers[i], numbers[i-window:i]):
            target = numbers[i]
            break
    print(target)

    # Part 2
    for i in range(limit):
        j = i 
        total = numbers[i]
        while total < target:
            j += 1
            total += numbers[j]
            if total == target:
                seq = sorted(numbers[i:j+1])
                print(seq[0] + seq[-1])
                return

def hasPairSum(target: int, numbers: list[int]) -> bool:
    for p in itertools.combinations(numbers, 2):
        if sum(p) == target: return True 
    return False

if __name__ == '__main__':
    do(solve)

'''
Part 1:
- Go through numbers starting from the 26th 
- With the current number as the target sum, consider the window of 25 numbers before it 
- Check if any combination of 2 numbers in the window sums up to the target 
- Find the first number which doesn't have a pair sum

Part 2: 
- With the target number from Part 1, find a window of contiguous numbers that sums up to it 
- Go through all positions until we find the correct window 
- Starting at current index, start growing the window, summing up the values 
- If the total is equal to the target, we have found the sequence:
  sort it and get the sum of the smallest and biggest numbers 
- If the total is already greater than target, window has burst so move on to next index
'''