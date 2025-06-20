# Advent of Code 2024 Day 07
# John Roy Daradal 

from aoc import *

Config = tuple[int, list[int]]

def data(full: bool) -> list[Config]:
    def fn(line: str) -> Config:
        head, tail = splitStr(line, ':')
        numbers = toIntList(tail, None)
        return int(head), numbers
    return [fn(line) for line in readLines(24, 7, full)]

def solve() -> Solution:
    configs = data(full=True)

    # Part 1
    score1 = scoreFn(useConcat=False)
    total1 = getTotal(configs, score1)

    # Part 2
    score2 = scoreFn(useConcat=True)
    total2 = getTotal(configs, score2)

    return newSolution(total1, total2)

def scoreFn(useConcat: bool) -> Callable:
    def scoreOf(cfg: Config) -> int:
        goal, numbers = cfg 
        return goal if isPossible(goal, numbers, useConcat) else 0
    return scoreOf

def isPossible(goal: int, numbers: list[int], useConcat: bool) -> bool:
    q = [numbers[0]]
    for y in numbers[1:]:
        q2 = []
        for x in q:
            q2.append(x + y)
            q2.append(x * y)
            if useConcat: q2.append(int('%d%d' % (x,y)))
        q = q2
    return goal in q

if __name__ == '__main__':
    do(solve, 24, 7)

'''
Solve:
- Compute the sum of the goals that can possibly be formed using left-to-right computation
- LHS = items in the queue; start with only first number in the queue 
- RHS = go through numbers in the queue, excluding the first 
- Update the queue by adding x + y, x * y, xy (Part2) in the queue (to explore all combinations)
- After getting all results, check if the goal number is included
- For Part 1, only use addition and multiplication
- For Part 2, include concatenation of the 2 digits
'''