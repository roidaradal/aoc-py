# Advent of Code 2016 Day 23
# John Roy Daradal 

from aoc import *

Command = tuple[str, int|str, int|str]

OPP: dict[str, str] = {
    'inc' : 'dec',
    'dec' : 'inc',
    'tgl' : 'inc',
    'jnz' : 'cpy', 
    'cpy' : 'jnz',
}

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
                return (cmd, reg, 0)
            case 'tgl':
                jmp = tryParseInt(p[1])
                return (cmd, jmp, 0)
        return ('?', 0, 0)
    return [fn(line) for line in readLines(16, 23, full)]

def solve() -> Solution:
    commands = data(full=True)

    # Part 1 
    value = runCommands(commands)

    # Part 2 
    total = 1
    for i in range(12): total *= (i+1)
    f1, f2 = 1, 1 
    if type(commands[19][1]) == int:
        f1 = commands[19][1]
    if type(commands[20][1]) == int:
        f2 = commands[20][1]
    total += f1 * f2

    return newSolution(value, total)

def runCommands(commands: list[Command]) -> int:
    idx, limit = 0, len(commands)
    reg = {k: 0 for k in 'abcd'}
    reg['a'] = 7
    while idx < limit:
        jmp = 1
        cmd, p1, p2 = commands[idx]
        if cmd == 'inc' or cmd == 'dec':
            if type(p1) == str:
                adj = 1 if cmd == 'inc' else -1
                reg[p1] += adj
        elif cmd == 'cpy':
            value = reg[p1] if p1 in reg else p1 
            if type(p2) == str and type(value) == int:
                reg[p2] = value
        elif cmd == 'jnz':
            cond = reg[p1] if p1 in reg else p1 
            value = reg[p2] if p2 in reg else p2
            if type(cond) == int and type(value) == int:
                jmp = value if cond != 0 else 1
        elif cmd == 'tgl':
            offset = reg[p1] if p1 in reg else p1 
            if type(offset) == int:
                idx2 = idx + offset
                if 0 <= idx2 < limit:
                    cmd2, arg1, arg2 = commands[idx2]
                    commands[idx2] = (OPP[cmd2], arg1, arg2)
        idx += jmp

    return reg['a']

if __name__ == '__main__':
    do(solve, 16, 23)

'''
Part1:
- Similar to the program in 1612 with instruction set: inc, dec, cpy, jnz
- Starts B,C,D registers at 0, but register A = 7
- New command: tgl flips the command offset away from it
    - inc becomes dec, while dec and tgl becomes inc 
    - jnz becomes cpy, while cpy becomes jnz
- If the offset is referencing an invalid command (out-of-bounds), ignore it
- If any of the commands cannot be run (because it was toggled and now the params dont make sense), skip it
- Run the commands in order, and output the contents of register A after processing 

Part2:
- Analyzed the two input datasets: two things that vary are the values in 
  command 19 and command 20; everything else is the same
- Manually analyzed the program to understand the behavior of the machine code
- Commands 0 - 18: finding the product of 12x11x10x...x2x1 (since we start register A = 12)
- Along the way, command 16 toggles the ff. commands:
    - 24: inc to dec
    - 22: inc to dec
    - 20: jnz to cpy
    - 18: jnz to cpy, this stops the loop
- Commands 19 - 25: adds the product of the param1 in command 19 and 20
- Example: cmd19 = cpy 71 c, cmd20 = cpy 72 d, add 71*72 to the product above
'''