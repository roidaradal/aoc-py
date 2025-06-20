# Advent of Code 2022 Day 09
# John Roy Daradal 

from aoc import *

Step = tuple[delta,int]

def data(full: bool) -> list[Step]:
    def fn(line: str) -> Step:
        head, tail = line.split()
        d = int(tail)
        if head == 'U':
            return U, d
        elif head == 'D':
            return D, d
        elif head == 'L':
            return L, d
        elif head == 'R':
            return R, d
        else:
            return (0,0), 0
    return [fn(line) for line in readLines(22, 9, full)]

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    steps = data(full=True)
    head, tail = (0,0), (0,0)
    visited: set[coords] = set([tail])
    for step in steps:
        head, tail = moveRope(head, tail, step, visited)
    return len(visited)

def part2() -> int:
    steps = data(full=True)
    tail = 9
    pos = [(0,0) for _ in range(tail+1)]
    visited: set[coords] = set([pos[tail]])
    for step in steps:
        pos = moveChain(pos, step, visited)
    return len(visited)

def moveRope(head: coords, tail: coords, step: Step, visited: set[coords]) -> tuple[coords, coords]:
    d, count = step 
    for _ in range(count):
        head = move(head, d)
        if not isAdjacent(head, tail):
            tail = follow(head, tail)
            visited.add(tail)
    return head, tail

def moveChain(pos: list[coords], step: Step, visited: set[coords]) -> list[coords]:
    tail = len(pos)-1
    d, count = step 
    for _ in range(count):
        pos[0] = move(pos[0], d)
        for i in range(1,tail+1):
            if not isAdjacent(pos[i-1], pos[i]):
                pos[i] = follow(pos[i-1], pos[i])
        visited.add(pos[tail])
    return pos

def isAdjacent(head: coords, tail: coords) -> bool:
    (y1,x1),(y2,x2) = head, tail 
    dy, dx = abs(y2-y1), abs(x2-x1)
    return dy <= 1 and dx <= 1

def follow(head: coords, tail: coords) -> coords:
    (y1,x1),(y2,x2) = head, tail 
    dy = y1-y2 
    if dy > 0:
        y2 += 1
    elif dy < 0:
        y2 -= 1
    dx = x1-x2 
    if dx > 0:
        x2 += 1
    elif dx < 0:
        x2 -= 1
    return y2, x2
    
if __name__ == '__main__':
    do(solve, 22, 9)

'''
Part1:
- Start with head and tail at (0,0)
- Keep track of the coords visited by the tail 
- Perform the steps by moving the head according to the delta and count 
- After moving the head, if the tail is not adjacent to the head, make it follow in the direction of the head
- Output the number of visited coords by the tail

Part2:
- Initialize the chain's positions all at (0,0)
- Keep track of the coords visited by the tail, similar to Part 1
- Perform the steps by moving the head of the chain, according to the delta and count
- Then, for each part of the chain, if it's position is not adjacent to the previous, make it follow the direction of the previous
- Output the number of visited coords by the tail
'''