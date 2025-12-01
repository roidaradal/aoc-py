# Advent of Code 2025 Day 01
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int2]:
    def fn(line: str) -> int2:
        sign = 1 if line[0] == 'R' else -1 
        return (sign, int(line[1:]))
    return [fn(line) for line in readLines(25, 1, full)]

def solve() -> Solution:
    moves = data(full=True)

    # Part 1 and 2
    count1, count2 = 0, 0 
    curr = 50 
    for sign, repeat in moves:
        for _ in range(repeat):
            curr = (curr + sign) % 100
            if curr == 0:
                count2 += 1
        if curr == 0:
            count1 += 1
    
    return newSolution(count1, count2)


if __name__ == '__main__':
    do(solve, 25, 1)

'''
Solve:
- Read the moves from input: -1 if L, 1 if R
- Start at 50, go through the moves and process them
- Repeat the steps of adding the sign to current number % 100 (wrap-around)
- For Part 1, increment the count if we get 0 after doing the full loop
- For Part 2, increment the count if we get 0 anytime during the loop
'''