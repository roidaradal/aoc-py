# Advent of Code 2023 Day 08
# John Roy Daradal 

from aoc import *
from math import lcm 

Pair = tuple[str,str]

T = {'L': 0, 'R': 1}
start, goal = 'AAA', 'ZZZ'

def data(full: bool) -> tuple[list[int], dict[str,Pair]]:
    lines = readLines(23, 8, full)
    moves = [T[x] for x in lines[0]]
    m: dict[str,Pair] = {}
    for line in lines[2:]:
        key, tail = splitStr(line, '=')
        a,b = splitStr(tail.strip('()'), ',')
        m[key] = (a,b)
    return moves, m

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    moves, m = data(full=True)
    limit = len(moves)
    count, i = 0, 0
    curr = start
    while curr != goal: 
        idx = moves[i]
        curr = m[curr][idx]
        count += 1
        i = (i+1) % limit 
    return count

def part2() -> int:
    moves, m = data(full=True)
    limit = len(moves)
    starts = [x for x in m if x.endswith('A')]
    counts = []
    for curr in starts:
        count, i = 0, 0
        while not curr.endswith('Z'):
            idx = moves[i]
            curr = m[curr][idx]
            count += 1
            i = (i+1) % limit 
        counts.append(count)
    return lcm(*counts)

if __name__ == '__main__':
    do(solve, 23, 8)

'''
Part1:
- Go through the L/R moves in order, wrapping around if necessary
- Starting from AAA, follow the conversion moves (L/R) to transform the current word
- Stop if we reach goal = ZZZ; output number of steps needed to reach goal

Part2:
- Similar to Part 1, but instead of only 1 starting point (AAA), we start at all words ending in A
- Compute the number of steps need from starting word to a word that ends with Z (not necessarily ZZZ)
- Idea: number of steps to reach from xxA -> xxZ is same number of steps from xxZ -> xxZ, so finding the
  first ends-with-Z word is enough to find the loop length of that word
- Find the LCM of all the counts to get the number of steps needed to make all words align and end in Z
'''