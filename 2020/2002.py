# Advent of Code 2020 Day 02
# John Roy Daradal 

from aoc import *

class Password:
    def __init__(self, line: str):
        head, tail = splitStr(line, ':')
        p = head.split()
        self.num1, self.num2 = toIntList(p[0], '-')
        self.char = p[1]
        self.text = tail

def data(full: bool) -> list[Password]:
    return [Password(line) for line in readLines(20, 2, full)]

def solve() -> Solution:
    passwords = data(full=True)

    # Part 1
    count1 = countValid(passwords, isValid)

    # Part 2
    count2 = countValid(passwords, isValid2)

    return newSolution(count1, count2)

def isValid(p: Password) -> bool:
    freq = charFreq(p.text)
    return p.num1 <= freq[p.char] <= p.num2

def isValid2(p: Password) -> bool:
    count = 0 
    for idx in [p.num1-1, p.num2-1]:
        if p.text[idx] == p.char:
            count += 1
    return count == 1


if __name__ == '__main__':
    do(solve, 20, 2)

'''
Part1:
- Valid if frequency of char is within range of num1, num2 inclusive

Part2:
- Valid if exactly 1 of the num1, num2 as the index has char
- Subtract 1 from num1, num2 because it is using 1-index
'''