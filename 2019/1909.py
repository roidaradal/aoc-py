# Advent of Code 2019 Day 09
# John Roy Daradal 

from aoc import *
from intcode import *

def data(full: bool) -> dict[int,int]:
    line = readFirstLine(19, 9, full)
    numbers = toIntList(line, ',')
    memory = defaultdict(int)
    for i,x in enumerate(numbers):
        memory[i] = x 
    return memory

def solve() -> Solution:
    # Part 1
    numbers = data(full=True)
    out1 = runProgram(numbers, 1) 

    # Part 2 
    numbers = data(full=True)
    out2 = runProgram(numbers, 2) 

    return newSolution(out1, out2)

def runProgram(numbers: dict[int, int], start: int) -> int:
    i, rbase = 0, 0 
    output = 0
    while True:
        word = str(numbers[i])
        head, tail = word[:-2], word[-2:]
        cmd = int(tail)
        if cmd == 99: break 

        if cmd in (1,2,7,8): # Add, Multiply, LessThan, Equals
            in1, in2, out = numbers[i+1], numbers[i+2], numbers[i+3]
            m1, m2, m3 = modes(head, 3)
            a = param2(in1, m1, rbase, numbers)
            b = param2(in2, m2, rbase, numbers)
            c = index(out, m3, rbase)
            if cmd == 1:
                numbers[c] = a + b
            elif cmd == 2:
                numbers[c] = a * b
            elif cmd == 7: 
                numbers[c] = 1 if a < b else 0
            elif cmd == 8:
                numbers[c] = 1 if a == b else 0
            i += 4
        elif cmd == 3: # Input
            m = modes(head, 1)[0]
            idx = index(numbers[i+1], m, rbase)
            numbers[idx] = start
            i += 2
        elif cmd == 4: # Output
            m = modes(head, 1)[0]
            output = param2(numbers[i+1], m, rbase, numbers)
            i += 2 
        elif cmd == 9: # relative base 
            m = modes(head, 1)[0]
            jmp = param2(numbers[i+1], m, rbase, numbers)
            rbase += jmp 
            i += 2
        elif cmd == 5 or cmd == 6: #Jump-if-True/False
            p1, p2 = numbers[i+1], numbers[i+2]
            m1, m2 = modes(head, 2)
            isZero = param2(p1, m1, rbase, numbers) == 0
            doJump = isZero if cmd == 6 else (not isZero)
            if doJump:
                i = param2(p2, m2, rbase, numbers)
            else:
                i += 3
    return output

if __name__ == '__main__':
    do(solve, 19, 9)

'''
RunProgram:
- Similar to 1905 IntCode program, with few additions
- Start with rbase (relative base) at 0
- If cmd == 9: update the rbase value
- All operations with indexes will now have to check if it is using the normal mode or relative mode
- Use param2 instead of param, as it considers relative base if mode is 2
- For Part 1, start with input = 1; for Part 2, start with input = 2
'''