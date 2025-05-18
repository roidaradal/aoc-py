# Advent of Code 2019 Day 05
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int]:
    line = readLines(19, 5, full)[0]
    return toIntList(line, ',')

def part1():
    numbers = data(full=True)
    runProgram(numbers, 1) 

def part2():
    numbers = data(full=True)
    runProgram(numbers, 5) 

def runProgram(numbers: list[int], start: int):
    i = 0 
    while True:
        word = str(numbers[i])
        head, tail = word[:-2], word[-2:]
        cmd = int(tail)
        if cmd == 99: break 

        if cmd in (1,2,7,8): # Add, Multiply, LessThan, Equals
            in1, in2, out = numbers[i+1:i+4]
            m1, m2, _ = modes(head, 3)
            a = param(in1, m1, numbers)
            b = param(in2, m2, numbers)
            if cmd == 1:
                numbers[out] = a + b
            elif cmd == 2:
                numbers[out] = a * b
            elif cmd == 7: 
                numbers[out] = 1 if a < b else 0
            elif cmd == 8:
                numbers[out] = 1 if a == b else 0
            i += 4
        elif cmd == 3: # Input
            idx = numbers[i+1]
            numbers[idx] = start
            i += 2
        elif cmd == 4: # Output
            m = modes(head, 1)[0]
            out = param(numbers[i+1], m, numbers)
            if out != 0: print(out)
            i += 2 
        elif cmd == 5 or cmd == 6: #Jump-if-True/False
            p1, p2 = numbers[i+1], numbers[i+2]
            m1, m2 = modes(head, 2)
            isZero = param(p1, m1, numbers) == 0
            doJump = isZero if cmd == 6 else (not isZero)
            if doJump:
                i = param(p2, m2, numbers)
            else:
                i += 3

def modes(cmd: str, count: int) -> list[int]: 
    m = [0] * count
    if len(cmd) == 0: return m

    i = 0
    for x in reversed(cmd):
        m[i] = int(x)
        i += 1
    return m

def param(x: int, mode: int, numbers: list[int]) -> int:
    return numbers[x] if mode == 0 else x

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
RunProgram:
- cmd = last 2 digits of current number 
- head = everything but 2 digits of current number (used for parameter mode)
- if cmd == 99: break 
- if cmd is 1, 2, 7 or 8: (common processing for 3 params)
    - get param modes of next 3 numbers 
    - store result of operation into index=p3
    - if cmd == 1 (add): sum of p1, p2
    - if cmd == 2 (mul): product of p1, p2 
    - if cmd == 7 (lt ): 1 if p1 < p2 else 0 
    - if cmd == 8 (eq ): 1 if p1 == p2 else 0
    - move pointer by 4
- if cmd == 3 (input): 
    - put the start number into the idx found in the next number
    - move pointer by 2
- if cmd == 4 (output):
    - get the param mode of the next number and print if param is not 0
    - move pointer by 2
- if cmd is 5 or 6: (common processing for 2 params)
    - get param modes of next 2 numbers
    - check if p1 == 0 
    - if cmd == 5 (jump-if-true):
        - if not zero: make pointer = p2
        - else: move pointer by 3
    - if cmd == 6 (jump-if-false):
        - if zero: make pointer= p2 
        - else: move pointer by 3
        
Modes:
- Default mode = 0 
- Process from right-to-left, so go through the cmd head in reverse
- if mode 0, use x as index to numbers 
- if mode 1, use x as raw value
'''