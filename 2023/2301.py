# Advent of Code 2023 Day 01
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[str]:
    return readLines(23, 1, full)

def solve() -> Solution:
    lines = data(full=True)
    
    # Part 1
    total1 = getTotal(lines, extractDigits)

    # Part 2
    total2 = getTotal(lines, extractNumber)

    return newSolution(total1, total2)

def extractDigits(line: str) -> int:
    first, last = 0, 0 
    for x in line:
        digit = parseDigit(x)
        if digit != None:
            first, last = update(first, last, digit)
    return (first*10) + last

def extractNumber(line: str) -> int:
    first, last = 0, 0 
    for i in range(len(line)):
        digit = parseDigit(line[i])
        if digit != None:
            first, last = update(first, last, digit)
            continue 
        digit = parseNumber(line[i:])
        if digit != None:
            first, last = update(first, last, digit)
    return (first * 10) + last

def parseDigit(x: str) -> int|None:
    code = ord(x)
    if 48 <= code <= 57:
        return code-48 
    return None

numberWords: list[strInt] = [
    ('one',1),('two',2),('three',3),('four',4),('five',5),
    ('six',6),('seven',7),('eight',8),('nine',9),
]
def parseNumber(text: str) -> int|None:
    for word,number in numberWords:
        if text.startswith(word):
            return number 
    return None

def update(first: int, last: int, digit: int) -> tuple[int,int]:
    if first == 0: first = digit 
    last = digit 
    return first, last

if __name__ == '__main__':
    do(solve, 23, 1)

'''
Part1:
- Go through each character in line 
- If character is a digit (ord code is in range 48-57), update first and last digits

Part2:
- Go through each character index in line 
- Check first if char at index is a digit (similar to Part1)
- If not a digit, check if substring starting at index starts with a number word
- Update first and last digits accordingly
'''