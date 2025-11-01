# Advent of Code 2024 Day 21
# John Roy Daradal 

from functools import cache
from aoc import *

Pad = dict[str2, str]

def data(full: bool) -> list[str]:
    return readLines(24, 21, full)

def solve() -> Solution:
    codes = data(full=True)
    numPad, dirPad = createPads()

    # Part 1 
    total1 = part1(codes, numPad, dirPad)

    # Part2 
    total2 = part2(codes, numPad, dirPad)

    return newSolution(total1, total2)

def createPads() -> tuple[Pad, Pad]:
    numPad: list[str] = ['789','456','123','#0A']
    dirPad: list[str] = ['#^A', '<v>']

    def createPadGraph(pad: list[str]) -> Pad:
        gap: coords = (0,0)
        padCoords: dict[str, coords] = {}
        for row,line in enumerate(pad):
            for col,tile in enumerate(line):
                if tile == '#':
                    gap = (row,col)
                    continue 
                padCoords[tile]= (row,col)
        
        graph: Pad = {}
        for a, (y1,x1) in padCoords.items():
            for b, (y2,x2) in padCoords.items():
                path = ('<' * (x1-x2)) + ('v' * (y2-y1)) + ('^' * (y1-y2)) + ('>' * (x2-x1))
                if gap == (y1,x2) or gap == (y2,x1):
                    path = path[::-1]
                graph[(a,b)] = path + 'A'
        return graph
    
    numPadGraph = createPadGraph(numPad)
    dirPadGraph = createPadGraph(dirPad)
    return numPadGraph, dirPadGraph

def part1(codes: list[str], numPad: Pad, dirPad: Pad) -> int:
    def convert(code: str, pad: Pad) -> str:
        result: str = ''
        prev = 'A'
        for char in code:
            result += pad[(prev, char)]
            prev = char
        return result

    total = 0
    for origCode in codes:
        code = convert(origCode, numPad)
        code = convert(code, dirPad)
        code = convert(code, dirPad)
        total += int(origCode[:-1]) * len(code)
    return total

def part2(codes: list[str], numPad: Pad, dirPad: Pad) -> int:
    @cache 
    def computeLength(code: str, itersLeft: int, isFirst: bool) -> int:
        if itersLeft == 0: return len(code)
        prev = 'A'
        total = 0 
        pad: Pad = numPad if isFirst else dirPad
        for char in code:
            total += computeLength(pad[(prev,char)], itersLeft-1, False)
            prev = char
        return total

    total = 0
    for code in codes:
        total += int(code[:-1]) * computeLength(code, 26, True)
    return total

if __name__ == '__main__':
    do(solve, 24, 21)

'''
Solve:
- Burnout, used a Reddit solution to complete AOC 2024 
- Reference: https://www.reddit.com/r/adventofcode/comments/1hj2odw/comment/m4fjgyn/ 
'''