# Advent of Code 2017 Day 15
# John Roy Daradal 

from aoc import *

def data(full: bool) -> int2:
    line1, line2 = readLines(17, 15, full)
    a = int(line1.split()[-1])
    b = int(line2.split()[-1])
    return a, b

def solve():
    prevAB = data(full=True)
    
    # Part 1
    count1 = countMatches(prevAB, (0, 0), 40_000_000)

    # Part 2 
    count2 = countMatches(prevAB, (4, 8), 5_000_000)

    return newSolution(count1, count2)

def countMatches(prevAB: int2, multAB: int2, numSteps: int) -> int:
    prevA, prevB = prevAB 
    multA, multB = multAB
    factorA, factorB = 16807, 48271 
    
    genA = generator(prevA, factorA, multA)
    genB = generator(prevB, factorB, multB)
    count = 0 
    factor = 1_000_000
    for i in range(numSteps):
        if i % factor == 0: print(i // factor)
        a = next(genA)
        b = next(genB)
        if isMatch(a, b): count += 1
    return count

def generator(prev: int, factor: int, mult: int):
    magic = 2147483647
    while True:
        curr = (prev * factor) % magic
        prev = curr 
        if mult == 0 or curr % mult == 0:
            yield curr 

def isMatch(a: int, b: int) -> bool:
    x = binaryFilled(a, 16)
    y = binaryFilled(b, 16)
    return x[-16:] == y[-16:]

if __name__ == '__main__':
    do(solve, 17, 15)

'''
Solve:
- Setup the two generators: 
    prevA, prevB are from input (starting numbers),
    multA, multB = if 0 not checked, if non-zero, filters generator results to only be multiples of this number 
    factorA, factorB = fixed for A = 16807, B = 48271
- Run for the specified number of steps, get the next output from genA and genB:
    next number = (previous * factor) % 2147483647; remember previous for next result 
    if mult is non-zero, yield only values that are cleanly divided by mult
- Count the number of matched responses: a and b match if the last 16 digits of their binary representations are the same
- For Part 1, dont use multiples, and run for 40,000,000 steps 
- For Part 2, use multA=4, multB=8, and run for 5,000,000 steps
'''