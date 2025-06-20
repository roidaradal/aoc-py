# Advent of Code 2024 Day 03
# John Roy Daradal 

import re
from aoc import *

def data(full: bool) -> str:
    return ''.join(readLines(24, 3, full))

def solve() -> Solution:
    return newSolution(part1(), part2())

pattern = r'mul\([0-9]{1,3},[0-9]{1,3}\)'

def part1() -> int:
    text = data(full=True)
    commands = re.findall(pattern, text) 
    return getTotal(commands, execCommand)

def part2() -> int:
    text = data(full=True)
    commands = [(m.start(), m.group(0)) for m in re.finditer(pattern, text)]

    off = r"don't\(\)"
    on  = r"do\(\)"
    regions = [(0,True)]
    for pat,flag in [(off,False), (on,True)]:
        for m in re.finditer(pat, text):
            regions.append((m.start(), flag))
    regions.sort()

    ignore = [] 
    offStart = None 
    for start, flag in regions:
        if flag == False and offStart is None:
            offStart = start 
        elif flag == True and offStart is not None:
            ignore.append((offStart, start-1))
            offStart = None 
    if offStart is not None:
        ignore.append((offStart, len(text)-1))

    valid = lambda cmd: not any(x[0] <= cmd[0] <= x[1] for x in ignore)
    commands = [cmd[1] for cmd in commands if valid(cmd)]
    return getTotal(commands, execCommand)

def execCommand(cmd: str) -> int:
    cmd = cmd.strip('mul()')
    a,b = toIntList(cmd, ',')
    return a * b

if __name__ == '__main__':
    do(solve, 24, 3)

'''
Part1:
- Find all mul(x,y) patterns in the text 
- Multiply x and y, and get the total of these products

Part2:
- Find the mul(x,y) patterns, similar to Part 1, but take note of their index
- Find the ON and OFF switches: do() and don't()
- Sort the indexes of mixed ON and OFF switches 
- Form the ignore zones by getting the ranges started by an OFF index up to before an ON index
- Filter the mul(x,y) commands found earlier: they must not fall in any of the ignore zones
- Process the valid commands and get the total of the x*y products
'''