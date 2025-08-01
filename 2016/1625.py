# Advent of Code 2016 Day 25
# John Roy Daradal 

from aoc import *

Command = tuple[str, int|str, int|str]

def data(full: bool) -> list[Command]:
    def fn(line: str) -> Command:
        p = line.split()
        cmd = p[0]
        match cmd:
            case 'cpy':
                value = tryParseInt(p[1])
                reg = p[2]
                return (cmd, value, reg)
            case 'jnz':
                cond = tryParseInt(p[1])
                jmp = tryParseInt(p[2])
                return (cmd, cond, jmp)
            case 'inc' | 'dec':
                reg = p[1]
                return ('inc', reg, 1 if cmd == 'inc' else -1)
            case 'out':
                value = tryParseInt(p[1])
                return (cmd, value, 0)
        return ('?', 0, 0)
    return [fn(line) for line in readLines(16, 25, full)]

def solve() -> Solution:
    commands = data(full=True)
    goalLen = 10
    goal = [0,1] * (goalLen // 2)
    a = 0 
    while True:
        reg = {k: 0 for k in 'abcd'}
        reg['a'] = a
        idx, limit = 0, len(commands)
        out: list[int] = []
        while idx < limit:
            jmp = 1
            cmd, p1, p2 = commands[idx]
            if cmd == 'inc':
                if type(p1) == str and type(p2) == int:
                    reg[p1] += p2
            elif cmd == 'cpy':
                value = reg[p1] if p1 in reg else p1 
                if type(p2) == str and type(value) == int:
                    reg[p2] = value
            elif cmd == 'jnz':
                cond = reg[p1] if p1 in reg else p1 
                value = reg[p2] if p2 in reg else p2
                if type(cond) == int and type(value) == int:
                    jmp = value if cond != 0 else 1
            elif cmd == 'out':
                value = reg[p1] if p1 in reg else p1
                if type(value) == int:
                    out.append(value)
                    if len(out) == goalLen:
                        if out == goal:
                            return newSolution(a, "")
                        break
            idx += jmp 
        a += 1

if __name__ == '__main__':
    do(solve, 16, 25)

'''
Solve:
- Similar to the program in 1612 with instruction set: inc, dec, cpy, jnz
- New out command: outputs a value; we collect this into a list for checking
- Start with B,C,D registers at 0
- Find the value for A that will make the program output 0,1,0,1,0,1,... repeatedly
- Start with A = 0, then increment until we find the A value that outputs 
  5 pairs of 0,1 => sufficient to conclude that it will print out 0,1,.. infinitely
- Run the program until we get 10 outputs: check if it has 5 pairs of 0,1; 
  if not, we stop this iteration and move on to the next value of A
- No problem for Part 2
'''