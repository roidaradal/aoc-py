# Advent of Code 2025 Day 03
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[list[int]]:
    return [toIntLine(line) for line in readLines(25, 3, full)]

def solve() -> Solution:
    banks = data(full=True)
    total1 = sum(computeTotalJolt(bank, 2) for bank in banks)
    total2 = sum(computeTotalJolt(bank, 12) for bank in banks)
    return newSolution(total1, total2)

def computeTotalJolt(bank: list[int], numBat: int) -> int:
    N = len(bank)
    start = 0
    batteries = []
    for d in range(numBat):
        candidates = [(i, bank[i]) for i in range(start, N-numBat+d+1)]
        idx, battery = max(candidates, key=lambda x: (x[1], -x[0]))
        batteries.append(battery)
        start = idx+1
    return int(''.join(str(x) for x in batteries))

if __name__ == '__main__':
    do(solve, 25, 3)

'''
Solve:
- For Part 1, turn on 2 batteries
- For Part 2, turn on 12 batteries
- Sum up the total jolt for each bank
- To compute the total jolt for one bank:
    - Loop <numBat> times to select the batteries that will give max jolt 
    - For each index d, the candidate batteries range from start index to the index that will
      have enough space to complete the remaining batteries
    - This could be expressed as range(start, N) if i + (numBat - d - 1) < N:
        - range(start, N): from start index to the end 
        - But only if index + (numBat - d - 1) < N: from the number of required batteries, 
          we remove d-1 (d since this is now the dth battery, 1 for the current battery)
        - Rewriting the inequality: i < N-numBat+d+1
    - Select the maximum value battery from the candidates, make sure we use the -idx for max
      so we select the earliest idx for ties
    - Add the max battery to the digits
    - Start is initially 0, and moves to the previous battery index + 1 after each iteration
'''