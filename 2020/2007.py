# Advent of Code 2020 Day 07
# John Roy Daradal 

from aoc import *

Hierarchy = dict[str, list[strInt]]

def data(full: bool) -> Hierarchy:
    h: Hierarchy = {}
    for line in readLines(20, 7, full):
        head, tail = splitStr(line, 'contain')
        if tail == 'no other bags.': continue 
        color = ' '.join(head.split()[:-1]) # remove 'bags'
        bags = splitStr(tail, ',')
        h[color] = [bagCount(b) for b in bags]
    return h

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    h = data(full=True)
    parents: dict[str,list[str]] = defaultdict(list)
    for parentColor, bagCounts in h.items():
        for color, _ in bagCounts:
            parents[color].append(parentColor)
    valid = set()
    q = parents['shiny gold']
    while len(q) > 0:
        color = q.pop()
        valid.add(color)
        nxt = parents[color]
        if len(nxt) > 0: q.extend(nxt)
    return len(valid)

def part2() -> int:
    h = data(full=True)
    count = countInside('shiny gold', h)
    return count

def bagCount(text: str) -> strInt:
    p = text.split()
    color = ' '.join(p[1:-1]) # remove 'bags' 
    count = int(p[0])
    return color, count

def countInside(color: str, h: Hierarchy) -> int:
    total = 0 
    if color in h:
        for color2,count in h[color]:
            total += count + (count * countInside(color2, h))
    return total

if __name__ == '__main__':
    do(solve, 20, 7)

'''
Part1:
- Count all valid parents of shiny gold 
- Start by computing the parents list of a color based on the hierarchy 
- Start with shiny gold's parents in the queue 
- Process until the queue is empty 
- Remove color from queue and add to valid parents
- If color also has parents, add to queue

Part2:
- Count how many bags can be contained inside shiny gold
- Make countInside a recursive function
- Base case: if color has no children, return 0 
- If color has children, add their count to the total and count inside the child too
'''