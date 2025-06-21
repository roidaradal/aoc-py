# Advent of Code 2020 Day 15
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int]:
    return toIntList(readFirstLine(20, 15, full), ",")

def solve() -> Solution:
    # Part 1 
    numbers = data(True)
    spoken1 = nthSpoken(numbers, 2020)

    # Part 2 
    numbers = data(True)
    spoken2 = nthSpoken(numbers, 30_000_000)

    return newSolution(spoken1, spoken2)

def nthSpoken(numbers: list[int], goal: int) -> int:
    turn = 1 
    lastSpoken: dict[int,int] = {}
    for speak in numbers[:-1]:
        lastSpoken[speak] = turn 
        turn += 1 
    curr = numbers[-1]
    while turn < goal:
        if curr in lastSpoken:
            nxt = turn - lastSpoken[curr]
        else:
            nxt = 0 
        lastSpoken[curr] = turn 
        turn += 1 
        curr = nxt 
    return curr

if __name__ == '__main__':
    do(solve, 20, 15)

'''
Solve:
- Start with the initial numbers spoken (except the last)
- Remember when each number was last spoken
- Start with the last initial number as the current number
- If current number is already spoken, next number is gap between now and last time it was last spoken
- If current number is not yet spoken, next number is 0
- Increment the turn; stop if we have reached the goal turn number
- For Part 1, find the 2020th number spoken 
- For Part 2, find the 30 millionth number spoken
'''