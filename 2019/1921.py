# Advent of Code 2019 Day 21
# John Roy Daradal 

from aoc import *
from intcode import *

def data(full: bool) -> dict[int,int]:
    line = readFirstLine(19, 21, full)
    numbers = toIntList(line, ',')
    memory = defaultdict(int)
    for i,x in enumerate(numbers):
        memory[i] = x 
    return memory

def solve() -> Solution:
    # Part 1
    numbers = data(full=True)
    commands = [
        'NOT T T',
        'AND A T',
        'AND B T',
        'AND C T',
        'NOT T T',
        'OR D J',
        'AND T J',
        'WALK',
    ]
    output1 = runProgram(numbers, commands)

    # Part 2
    numbers = data(full=True)
    commands = [
        'NOT T T',
        'AND A T',
        'AND B T',
        'AND C T',
        'NOT T T',
        'OR D J',
        'AND T J',
        'NOT T T',
        'OR E T',
        'OR H T',
        'AND T J',
        'RUN',
    ]
    output2 = runProgram(numbers, commands)

    return newSolution(output1, output2)

def runProgram(numbers: dict[int, int], commands: list[str]) -> int:
    i, rbase = 0, 0 
    inputs: list[int] = []
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
            if len(inputs) == 0:
                cmd = '\n'.join(commands) + '\n'
                inputs = [ord(x) for x in cmd]
            numbers[idx] = inputs.pop(0)
            i += 2
        elif cmd == 4: # Output
            m = modes(head, 1)[0]
            output = param2(numbers[i+1], m, rbase, numbers)
            if output >= 128:
                return output
            # else: # Uncomment this if you want to see the output
            #     print(chr(output), end='')
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
    return 0

if __name__ == '__main__':
    do(solve, 19, 21)

'''
Solve:
- Similar to 1917 (ASCII Intcode), except for input and output:
    - For the input, if the list of input numbers are empty, join the list of springscript commands 
      by newline, and add a newline to the resulting string; then convert the characters to ASCII and
      these numbers will be fed to the input one at a time
    - For output, if the output number is not an ASCII character (>=128), return this value as the hull
      damage, otherwise, print the ASCII character one at a time (during debug mode)
- We have two writable registers: T (temporary) and J (jump), where J holds the decision of whether to jump or not
- Both writable registers are initialized to False
- When we jump, it takes 4 steps to land: (x+1,y-1), (x+2,y-2), (x+3,y-1), (x+4,y); need to make sure there is 
  ground 4 steps ahead when we jump so that we dont fall through
- For Part 1, we end the instruction list with a WALK command
    - We can see up to 4 tiles ahead, via the registers A (1), B (2), C (3), D (4 tiles ahead)
    - The core idea for our jumping decision is: if we see D as ground (True), and one of the 
      three tiles ahead are holes, we can jump now (safe since D = 4 steps away is ground)
    - Decision: (NOT A OR NOT B OR NOT C) AND D
    - Set T = is there a hole in any of the next 3 tiles?
        - NOT T T = set T to true
        - AND A T, AND B T, AND C T => T = (T AND A AND B AND C)
        - NOT T T = NOT (T AND A AND B AND C) = (False OR NOT A OR NOT B OR NOT C)
    - OR D J = jump is initially False, jump = True if D is ground (True)
    - AND T J = jump if D is ground AND there is a hole in any of the next 3 tiles
- For Part 2, we end the instruction list with a RUN command
    - Use the same base rule as Part 1 = jump if 4 tiles ahead is safe and there is a hole in the next 3 tiles
    - Augment the rule: safe to jump if either 5th tile or 8th tile is ground:
        - If 5th tile is hole (need to jump again immediately) and 8th tile is ground, we can safely jump in next round 
        - If 5th tile is ground, we don't need to immediately jump in the next round
    - NOT T T = reset T back to False if it was set to true in the first part 
    - OR E T = E can be ground (5th tile away)
    - OR H T = H can be ground (8th tile away)
    - AND T J = augment the jumping condition with the rule in T
'''