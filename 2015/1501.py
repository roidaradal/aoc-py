# Advent of Code 2015 Day 01
# John Roy Daradal 

from aoc import * 

T: dict[str,int] = {
    '(' : 1,
    ')' : -1,
}

def data(full: bool) -> str:
    return readLines(15, 1, full)[0]

def part1():
    line = data(full=True)
    level = process(line, None)
    print(level)

def part2():
    line = data(full=True)
    level = process(line, -1)
    print(level)

def process(line: str, goal: int|None) -> int:
    level = 0
    for i,x in enumerate(line):
        level += T[x]
        if level == goal:
            return i+1
    return level


if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Iterate through each character in line 
- If ( : increase level by 1 
- If ) : decrease level by 1

Part2:
- Same level processing in Part 1 
- If level == -1: output character index+1
'''