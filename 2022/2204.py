# Advent of Code 2022 Day 04
# John Roy Daradal 

from aoc import *

pair = tuple[int2, int2]

def data(full: bool) -> list[pair]:
    def fn(line: str) -> pair:
        p1, p2 = splitStr(line, ',')
        p1 = toInt2(p1, '-')
        p2 = toInt2(p2, '-')
        return (p1, p2)
    return [fn(line) for line in readLines(22, 4, full)]

def part1():
    pairs = data(full=True)
    count = countValid(pairs, isSupersetPair)
    print(count) 

def part2():
    pairs = data(full=True)
    count = countValid(pairs, isOverlappingPair)
    print(count) 

def isSupersetPair(p: pair) -> bool:
    r1, r2 = p
    return isSupersetRange(r1, r2) or isSupersetRange(r2, r1)

def isSupersetRange(r1: int2, r2: int2) -> bool:
    (s1,e1), (s2,e2) = r1, r2
    return s1 <= s2 and e2 <= e1

def isOverlappingPair(p: pair) -> bool:
    (s1,e1), (s2,e2) = p
    if s1 < s2:
        return s2 <= e1 
    else:
        return s1 <= e2


if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Count pairs where one is superset of another (check both ways)
- Range is superset of another if start and end of r2 is inside the range of start, end of r1

Part2:
- Count pairs that have overlapping ranges (check which range comes first)
- Overlapping if another range has started before the other ended
'''