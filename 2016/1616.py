# Advent of Code 2016 Day 16
# John Roy Daradal 

from aoc import *

def data(full: bool) -> str:
    return readFirstLine(16, 16, full)

def solve() -> Solution:
    bits = data(full=True)

    # Part 1
    check1 = findChecksum(bits, 272)

    # Part 2
    check2 = findChecksum(bits, 35651584)

    return newSolution(check1, check2)

def findChecksum(bits: str, maxSize: int) -> str:
    while len(bits) < maxSize:
        bits = dragonCurve(bits)
    bits = bits[:maxSize]
    return createChecksum(bits)

def dragonCurve(bits: str) -> str:
    a = bits 
    b = bits[::-1]
    b = ''.join('1' if x == '0' else '0' for x in b)
    return '%s0%s' % (a, b)

def createChecksum(bits: str) -> str:
    curr: list[str] = list(bits)
    while True:
        nxt = []
        for i in range(0, len(curr), 2):
            nxt.append('1' if curr[i] == curr[i+1] else '0')
        curr = nxt 
        if len(nxt) % 2 != 0: break
    return ''.join(curr)

if __name__ == '__main__':
    do(solve, 16, 16)

'''
Solve:
- For Part 1, find the checksum for disk size = 272 
- For Part 2, find the checksum for disk size = 35651584
- To find the checksum of the input data with the given disk size:
    - Transform the bits repatedly using DragonCurve until the length of the bits 
      is at least the disk size 
    - Take only the first diskSize digits of the produced bits 
    - Create the checksum for the resulting bits 
- To compute the dragon curve of given bits = a:
    - Let b = reversed a and flipped bits (1 <=> 0)
    - Return a0b 
- To compute the checksum of given bits, repeat until the checksum length is odd:
    - Check the non-overlapping pairs of digits: if equal, add 1, else 0 
    - The results form the next checksum; continue if length is still even
'''