# Advent of Code 2020 Day 25
# John Roy Daradal 

from aoc import *

def data(full: bool) -> int2:
    line1, line2 = readLines(20, 25, full)
    return int(line1), int(line2)

def solve() -> Solution:
    cardKey, doorKey = data(full=True)
    cardLoop = findLoopSize(cardKey, 7)
    encryptionKey = encrypt(doorKey, cardLoop)
    return newSolution(encryptionKey, "")

def findLoopSize(key: int, subject: int) -> int:
    steps = 0 
    value = 1 
    while value != key:
        value = (value * subject) % 20201227
        steps += 1
    return steps

def encrypt(subject: int, steps: int) -> int:
    value = 1 
    for _ in range(steps):
        value = (value * subject) % 20201227
    return value

if __name__ == '__main__':
    do(solve, 20, 25)

'''
Solve:
- With the card key as the target value, find the number of steps it takes to transform starting
  from 1 to the target value, by doing value = (value * 7) % 20201227
- Using the number of steps above as the card loop size, encrypt the door key by transforming the value
  starting from 1 by the specified loop size: value = (value * doorKey) % 20201227
- Output the encryption key produced by the second step
- No problem for Part 2
'''