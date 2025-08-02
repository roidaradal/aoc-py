# Advent of Code 2017 Day 23
# John Roy Daradal 

import math
from aoc import *

def data(full: bool) -> list[str3]:
    def fn(line: str) -> str3:
        p = splitStr(line, None)
        return (p[0], p[1], p[2])
    return [fn(line) for line in readLines(17, 23, full)]

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    commands = data(full=True)
    reg: dict[str,int] = {k: 0 for k in 'abcdefgh'}
    idx, limit = 0, len(commands)
    count = 0
    while True:
        cmd, p1, p2 = commands[idx]
        step = 1 
        match cmd:
            case 'set':
                reg[p1] = valueOf(p2, reg)
            case 'sub':
                reg[p1] -= valueOf(p2, reg)
            case 'mul':
                reg[p1] *= valueOf(p2, reg)
                count += 1
            case 'jnz':
                if valueOf(p1, reg) != 0:
                    step = valueOf(p2, reg)
        idx += step            
        if idx < 0 or idx >= limit: break 
    return count

def part2() -> int:
    count = 0
    for b in range(106_700, 123_701, 17):
        limit = math.ceil(math.sqrt(b)) + 1
        for d in range(2, limit):
            e = b // d 
            if d * e == b:
                count += 1
                break
    return count

def valueOf(x: str, reg: dict[str,int]) -> int:
    v = tryParseInt(x)
    return v if type(v) == int else reg[x]

if __name__ == '__main__':
    do(solve, 17, 23)

'''
Part1:
- Start the registers A-H at 0, start at command index=0
- For param2 of commands, use the literal value if it's an integer, otherwise it's a 
  letter, so use the value of the register with that name
- set command: reg[p1] = valueOf(p2)
- sub command: reg[p1] -= valueOf(p2)
- mul command: reg[p1] *= valueOf(p2)
- jnz command: if valueOf(p1) != 0, jump command index by valueOf(p2)
- If command index goes out of bounds, stop the loop 
- Return the number of times the mul command was called

Part2:
- Manually analyzed the program:
- From 106,700 to 123,700 incrementing by 17, count the number of non-prime numbers
- Register A: set to 1 to activate the setting of B, C values 
- Register B: stores the starting and current value of the main loop
- Register C: stores the ending value of the main loop
- Register D, E: stores the current factor1 and factor2 values being checked for number being prime
- Register F: flag for composite numbers (0 if found values for D*E that equals B)
- Register G: used to check for loop exit condition
- Register H: Counter for non-prime numbers; final value here is the final output
- 0-7: Sets b=(67*100)+100,000=106,700, Sets c=106,700+17,000 = 123,700
- 8: Initialize f flag to 1 (prime)
- 9: Start d = 2 (factor 1)
- 10: Start e = 2 (factor 2)
- 11-13: Sets g = (d*e)-b, to check if d*e == b
- 14-15: Set f flag to 0 (composite) if d*e == b (b is composite)
- 16: Increment e by 1 (for next factor)
- 17-19: Check if e has reached b, if not go back to command 11 (inner loop #2)
- 20: Increment d by 1 (for next factor)
- 21-23: Check if d has reached b, if not go back to command 10 (inner loop #1)
- 24-25: After exiting inner loop #1, check if f flag is composite (0), if it is, increment h (counter)
- 26-28: Check if b == c, if it is, exit the loop (#29)
- 30-31: If not, increment by 17, and jump back to command 8 (outer loop)
'''