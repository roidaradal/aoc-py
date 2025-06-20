# Advent of Code 2015 Day 01
# John Roy Daradal 

from aoc import * 

def data(full: bool) -> str:
    return readFirstLine(15, 1, full)

def solve() -> Solution:
    line = data(full=True)

    # Part 1
    level1 = process(line, None)

    # Part 2
    level2 = process(line, -1)

    return newSolution(level1, level2)

def process(line: str, goal: int|None) -> int:
    level = 0
    for i,x in enumerate(line):
        level += 1 if x == '(' else -1
        if level == goal:
            return i+1
    return level

if __name__ == '__main__':
    do(solve, 15, 1)

'''
Part1:
- Iterate through each character in line 
- If ( : increase level by 1 
- If ) : decrease level by 1

Part2:
- Same level processing in Part 1 
- If level == -1: output character index+1
'''