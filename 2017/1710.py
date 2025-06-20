# Advent of Code 2017 Day 10
# John Roy Daradal 

from aoc import *
from knotHash import *
from functools import reduce
from operator import xor

def data(full: bool) -> str:
    return readFirstLine(17, 10, full)

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    line = data(full=True)
    lengths = toIntList(line, ',')
    numbers = knotHash(lengths, 1)
    return numbers[0] * numbers[1]

def part2() -> str:
    line = data(full=True)
    lengths = [ord(x) for x in line]
    numbers = knotHash(lengths, 64)
    result = []
    for i in range(0, knotHashLimit, 16):
        r = reduce(xor, numbers[i:i+16])
        result.append(hexCode(r))
    return ''.join(result)

if __name__ == '__main__':
    do(solve, 17, 10)

'''
Part1:
- Compute KnotHash for 1 round using the lengths in the input
- Output the product of the first two numbers in the result

Part2:
- The lengths can be computed by treating each character in the input as an ASCII code 
- Add the other lengths specified
- Compute KnotHash for 64 rounds
- Take the resulting list of 256 numbers and process by chunks of size 16
- For each chunk, compute the xor of the 16 numbers (use reduce) and append its 2-digit hexcode to result
- Print out the 32-character result

KnotHash:
- Start with list of numbers from 0 to 255
- Start at index = 0, skip = 0
- Repeat process based on number of rounds specified; do not reset index, skip in between rounds
- Go through each length from the input; if length > 256, skip it
- Compute the span by adding the length to current index (i + length)
- If span is within normal bounds, reverse that span
- If need to wrap-around, combine the tail span and the head span and reverse it
- Put the reversed span back to the tail span and head span's positions
- Move the index by increasing it with the length and current skip; wrap-around if necessary
- Increase the skip after processing one length
'''