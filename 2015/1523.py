# Advent of Code 2015 Day 23
# John Roy Daradal 

from aoc import *

Command = tuple[str, int, int]

def data(full: bool) -> list[Command]:
    reg: dict[str, int] = {'a': 0, 'b': 1}
    def fn(line: str) -> Command:
        line = line.replace(',', '')
        p = splitStr(line, None)
        cmd = p[0]
        idx, offset = 0, 0
        match cmd:
            case 'hlf' | 'tpl' | 'inc':
                idx = reg[p[1]]
            case 'jmp':
                offset = int(p[1])
            case 'jie' | 'jio':
                idx = reg[p[1]]
                offset = int(p[2])
        return (cmd, idx, offset)
    return [fn(line) for line in readLines(15, 23, full)]

def solve() -> Solution:
    commands = data(full=True)

    # Part 1 and 2
    output: list[int] = []
    for a in [0, 1]: 
        reg = [a, 0]
        ip, limit = 0, len(commands)
        while ip < limit:
            cmd, idx, offset = commands[ip]
            jmp = 1
            match cmd:
                case 'hlf':
                    reg[idx] //= 2
                case 'tpl':
                    reg[idx] *= 3
                case 'inc':
                    reg[idx] += 1
                case 'jmp':
                    jmp = offset
                case 'jie':
                    if reg[idx] % 2 == 0:
                        jmp = offset
                case 'jio':
                    if reg[idx] == 1:
                        jmp = offset
            ip += jmp
        output.append(reg[1])
    
    b1, b2 = output
    return newSolution(b1, b2)


if __name__ == '__main__':
    do(solve, 15, 23)

'''
Solve:
- Commands are represented as (cmd, reg, offset), where reg is the idx of the register 
  to update (if any), while offset is for the jump commands
- Start with the instruction pointer (ip) at 0; unless a jump occurs, increment this ip by 1 after each command
- Process the current command, indexed by the the ip 
    - hlf:  reg[r] //= 2 
    - tpl:  reg[r] *= 3
    - inc:  reg[r] += 1
    - jmp:  set jump to offset 
    - jie   set jump to offset, if reg[r] is even 
    - jio   set jump to offset, if reg[r] is 1
- For Part 1, run the program with reg[A] = 0
- For Part 2, run the program with reg[A] = 1
- Output the value of reg[B] after running the program
'''