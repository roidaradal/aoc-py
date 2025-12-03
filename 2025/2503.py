# Advent of Code 2025 Day 03
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[list[int]]:
    return [toIntLine(line) for line in readLines(25, 3, full)]

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    banks = data(full=True)
    total = 0
    for bank in banks:
        limit = len(bank)
        maxJolt = 0
        for i, d1 in enumerate(bank):
            for j in range(i+1, limit):
                d2 = bank[j]
                jolt = (d1 * 10) + d2 
                maxJolt = max(maxJolt, jolt)
        total += maxJolt
    return total


def part2() -> int:
    banks = data(full=True)
    total = 0 
    for bank in banks:
        limit = len(bank)
        start = 0
        digits = []
        for d in range(12):
            remaining = 11-d
            candidates = [(i, bank[i]) for i in range(start, limit) if i + remaining < limit]
            best = max(candidates, key=lambda x: (x[1], -x[0]))
            idx = best[0]
            digits.append(best[1])
            start = idx+1
        total += int(''.join(str(x) for x in digits))
    return total

if __name__ == '__main__':
    do(solve, 25, 3)

'''
Part1:
- Go through each bank and find the max jolt for bank
- For the first digit, go through each digit of bank
- For the second digit, go through each digit after the first digit 
- Combine the two digits, and find the maximum jolt from the digit combinations 
- Return total max jolt 

Part2:
- Go through each bank and find max jolt for bank, same as in Part 1 
- Build the 12 digits by starting at index 0:
    - For each digit index d, compute the remaining digits after (11-d)
    - The candidate digits are those in indices from (start, limit) but only if 
      index i + remaining digits < limit (can still build remaining digits)
    - Find the maximum digit out of the candidates, noting their index too 
    - Add max digit to the digits list, and move the start index for next round 
      to index+1
    - Combine the 12 digits to form the max jolt number
- Return total max jolt
'''