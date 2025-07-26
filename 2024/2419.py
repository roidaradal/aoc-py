# Advent of Code 2024 Day 19
# John Roy Daradal 

from functools import cache
from aoc import *

patterns: list[str] = []

def data(full: bool) -> tuple[list[str], list[str]]:
    lines = readLines(24, 19, full)
    patterns = splitStr(lines[0], ',')
    designs = lines[2:]
    return patterns, designs

def solve() -> Solution:
    global patterns
    patterns, designs = data(full=True)

    valid, total = 0, 0
    for design in designs:
        count = countPossible(design)
        if count > 0:
            valid += 1      # Part 1 
            total += count  # Part 2
    
    return newSolution(valid, total)

@cache 
def countPossible(design: str) -> int:
    if design == '': return 1

    tails: list[str] = []
    for pattern in patterns:
        if design.startswith(pattern):
            tail = design[len(pattern):]
            tails.append(tail)
    return sum(countPossible(tail) for tail in tails)

if __name__ == '__main__':
    do(solve, 24, 19)

'''
Solve:
- Make the list of patterns a global variable so it can be accessed by the memoized function countPossible 
- For each design, count the number of possible breakdowns from the patterns
    - Use memoized recursion (functools.cache), as the subproblems would be overlapping 
    - Base case: if design is empty, return 1
    - Go through each pattern: if design has pattern as the prefix, we take the tail (removing the prefix)
    - Call countPossible recursively on each of the tails and return their total
- If count > 0, increment the valid count for Part 1
- Return the total possible counts for all designs for Part 2
'''