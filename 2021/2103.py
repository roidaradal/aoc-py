# Advent of Code 2021 Day 03
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[str]:
    return readLines(21, 3, full)

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    binaryNumbers = data(full=True)
    count = defaultdict(int)
    for code in binaryNumbers:
        for i,bit in enumerate(code):
            if bit == '1':
                count[i] += 1
    mid = len(binaryNumbers) // 2 
    g, e = [], []
    for i in range(len(binaryNumbers[0])):
        if count[i] > mid:
            g.append('1')
            e.append('0')
        else:
            g.append('0')
            e.append('1')
    g = int(''.join(g), 2)
    e = int(''.join(e), 2)
    return g * e

def part2() -> int:
    binaryNumbers = data(full=True)
    oxy = filterMax(binaryNumbers)
    co2 = filterMin(binaryNumbers)
    return oxy * co2

def filterMax(binaryNumbers: list[str]) -> int:
    bitLength = len(binaryNumbers[0])
    for i in range(bitLength):
        c1 = countIndex(binaryNumbers, i)
        c0 = len(binaryNumbers) - c1 
        maxBit = '1' if c1 >= c0 else '0'
        binaryNumbers = [code for code in binaryNumbers if code[i] == maxBit]
        if len(binaryNumbers) == 1: break 
    return int(binaryNumbers[0], 2)

def filterMin(binaryNumbers: list[str]) -> int: 
    bitLength = len(binaryNumbers[0])
    for i in range(bitLength):
        c1 = countIndex(binaryNumbers, i)
        c0 = len(binaryNumbers) - c1 
        minBit = '0' if c0 <= c1 else '1'
        binaryNumbers = [code for code in binaryNumbers if code[i] == minBit]
        if len(binaryNumbers) == 1: break 
    return int(binaryNumbers[0], 2)

def countIndex(binaryNumbers: list[str], index: int) -> int:
    return sum(1 for code in binaryNumbers if code[index] == '1')

if __name__ == '__main__':
    do(solve, 21, 3)

'''
Part1:
- Count the frequency of 1 at each bit position
- Form the gamma end epsilon by checking the freq of 1 at each bit 
- If more 1s at index, gamma at this bit is 1, epsilon is 0 
- If more 0s at index, gamma at this bit is 0, epsilon is 1 
- Since we are only keeping track of 1's count, we can check if 
  more 1s if the count > mid (e.g. 12 bits, if count is 7, more 1s)

Part2:
- filterMax: repeatedly filter out codes until we are left with only one 
- Process each bit index: at this index, check if there are more 1s than 0s
- Only keep the binary codes whose bit at current index is same as the maxBit
- Note: len(binaryNumbers) changes per iteration so we shouldnt make a variable outside loop for this
- Do the same for filterMin, but keep the codes whose bit at the index is the minBit
'''