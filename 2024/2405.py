# Advent of Code 2024 Day 05
# John Roy Daradal 

from aoc import *

def data(full: bool) -> tuple[dict[int,set[int]], list[list[int]]]:
    rules, pages = [], []
    part2 = False
    for line in readLines(24, 5, full):
        if part2:
            pages.append(toIntList(line, ','))
        elif line == '':
            part2 = True 
        else:
            a,b = toIntList(line, '|')
            rules.append((a,b))
    book = defaultdict(set)
    for before,after in rules:
        book[after].add(before)
    return book, pages

def solve() -> Solution:
    rules, pages = data(full=True)

    # Part 1
    fn1 = lambda numbers: numbers[len(numbers)//2] if isValid(numbers, rules) else 0
    total1 = getTotal(pages, fn1)

    # Part 2
    fn2 = lambda numbers: correctOrderMid(numbers, rules)
    total2 = getTotal(pages, fn2) 

    return newSolution(total1, total2)

def isValid(numbers: list[int], rules: dict[int,set[int]]) -> bool:
    for i in range(len(numbers)-1):
        after = set(numbers[i+1:])
        blacklist = rules[numbers[i]]
        common = after.intersection(blacklist)
        if len(common) > 0: return False 
    return True

def correctOrderMid(numbers: list[int], rules: dict[int,set[int]]) -> int:
    valid = True 
    idx, limit = 0, len(numbers)-1 
    while idx < limit:
        curr = numbers[idx]
        after = set(numbers[idx+1:])
        blacklist = rules[curr]
        common = after.intersection(blacklist)
        if len(common) == 0:
            idx += 1
        else:
            valid = False 
            insert = max(numbers.index(x) for x in common) + 1 
            numbers[idx] = 0 
            numbers = numbers[:insert] + [curr] + numbers[insert:]
            numbers.remove(0)
    return 0 if valid else numbers[len(numbers)//2]

if __name__ == '__main__':
    do(solve, 24, 5)

'''
Part1:
- Rulebook for a page number indicates its dependencies (should be printed before it)
- Check if the pages are in the correct order
- Sum up the middle pages of the numbers in valid order
- To check if valid, go through each number except last (no after)
- Check if any of the numbers after current are in the current number's blacklist (dependency)

Part2:
- Try to correct the page orders of those that are in invalid order 
- Sum up the corrected middle pages of the numbers in invalid order, after correcting them
- Do the check for order correctness similar to Part 1 
- If not in correct order, find the furthest index you can move that number after 
- Move that number so that all its dependencies come before it
'''