# Advent of Code 2016 Day 12
# John Roy Daradal 

from aoc import *

Command = tuple[str, int|str, int|str]

def data(full: bool) -> list[Command]:
    def fn(line: str) -> Command:
        p = line.split()
        cmd = p[0]
        if cmd == 'cpy':
            reg = p[2]
            value = tryParseInt(p[1])
            return (cmd, reg, value)
        elif cmd == 'jnz':
            jmp = int(p[2])
            cond = tryParseInt(p[1])
            return (cmd, cond, jmp)
        elif cmd == 'inc' or cmd == 'dec':
            jmp = 1 if cmd == 'inc' else -1 
            reg = p[1]
            return ('inc', reg, jmp)
        return ('?', 0, 0)
    return [fn(line) for line in readLines(16, 12, full)]

def solve():
    commands = data(full=True)
    limit = len(commands)
    overrides: list[None|dict[str,int]] = [None, {'c': 1}]
    for override in overrides:
        reg = {k: 0 for k in 'abcd'}
        if override != None:
            reg.update(override)
        idx = 0 
        while idx < limit:
            cmd, p1, p2 = commands[idx]
            if cmd == 'inc':
                if type(p1) == str and type(p2) == int:
                    reg[p1] += p2
                    idx += 1
            elif cmd == 'cpy':
                value = reg[p2] if p2 in reg else p2
                if type(p1) == str and type(value) == int:
                    reg[p1] = value 
                    idx += 1
            elif cmd == 'jnz':
                value = reg[p1] if p1 in reg else p1 
                if type(value) == int and type(p2) == int:
                    jmp = p2 if value != 0 else 1
                    idx += jmp
        print(reg['a'])

if __name__ == '__main__':
    do(solve)

'''
Solve:
- Initialize the a,b,c,d registers to 0 
- Start at the first command, loop until we go out of bounds
- For inc commands, increment the register by the specified amount, move the command index by 1
- For cpy commands, check whether the value is a literal or from another register;
  then overwrite the specified register by that value, move the command index by 1 
- For jnz commands, check whether the value for the condition is a literal or from another register,
  then check if the value is zero; if it is, move the command index by the jump amount, otherwise just move by 1
- Output the contents of register 'a' after exiting the loop
- For Part 2, initialize the register c to 1
'''