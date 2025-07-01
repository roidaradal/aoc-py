# Advent of Code 2018 Day 19
# John Roy Daradal 

from aoc import *

Instruction = tuple[str, int, int, int]

def data(full: bool) -> tuple[int, list[Instruction]]:
    ip: int = 0 
    instructions: list[Instruction] = []
    for line in readLines(18, 19, full):
        if line.startswith('#ip'):
            ip = int(line.split()[1])
        else:
            cmd, a, b, c = splitStr(line, None)
            instructions.append((cmd, int(a), int(b), int(c)))
    return ip, instructions

def solve() -> Solution:
    ip, instructions = data(full=True)

    # Part 1 
    value1 = executeInstructions(ip, instructions, [0,0,0,0,0,0])
    

    # Part 2 
    value2 = executeInstructions(ip, instructions, [1,0,0,0,0,0], breakOnIndex=3, targetIndex=2)
    # Note: use analyzeProgram first to determine the breakIndex and targetIndex

    return newSolution(value1, value2)

def execute(instruction: Instruction, reg: list[int]):
    cmd, a, b, c = instruction 
    match cmd:
        case 'addr':
            reg[c] = reg[a] + reg[b]
        case 'addi':
            reg[c] = reg[a] + b
        case 'mulr':
            reg[c] = reg[a] * reg[b]
        case 'muli':
            reg[c] = reg[a] * b 
        case 'banr':
            reg[c] = reg[a] & reg[b]
        case 'bani':
            reg[c] = reg[a] & b
        case 'borr':
            reg[c] = reg[a] | reg[b]
        case 'bori':
            reg[c] = reg[a] | b
        case 'setr':
            reg[c] = reg[a]
        case 'seti':
            reg[c] = a
        case 'gtir':
            reg[c] = 1 if a > reg[b] else 0
        case 'gtri':
            reg[c] = 1 if reg[a] > b else 0
        case 'gtrr':
            reg[c] = 1 if reg[a] > reg[b] else 0
        case 'eqir':
            reg[c] = 1 if a == reg[b] else 0
        case 'eqri':
            reg[c] = 1 if reg[a] == b else 0
        case 'eqrr':
            reg[c] = 1 if reg[a] == reg[b] else 0

def executeInstructions(ip: int, instructions: list[Instruction], reg: list[int], breakOnIndex: int = -1, targetIndex: int = 0) -> int:
    limit = len(instructions)
    while True:
        idx = reg[ip]
        if breakOnIndex >= 0 and idx == breakOnIndex: break

        execute(instructions[idx], reg)
        idx = reg[ip] + 1
        if 0 <= idx and idx < limit: # valid 
            reg[ip] = idx 
        else:
            break

    if breakOnIndex >= 0:
        target = reg[targetIndex]
        total = 0
        for i in range(1, target+1):
            if target % i == 0:
                total += i 
        return total
    else:
        return reg[0]

def analyzeProgram():
    display = {
        'addr': lambda a,b,c: f'r{c} = r{a} + r{b}', 
        'addi': lambda a,b,c: f'r{c} = r{a} + {b}', 
        'mulr': lambda a,b,c: f'r{c} = r{a} * r{b}', 
        'muli': lambda a,b,c: f'r{c} = r{a} * {b}', 
        'banr': lambda a,b,c: f'r{c} = r{a} & r{b}', 
        'bani': lambda a,b,c: f'r{c} = r{a} & {b}', 
        'borr': lambda a,b,c: f'r{c} = r{a} | r{b}', 
        'bori': lambda a,b,c: f'r{c} = r{a} | {b}', 
        'setr': lambda a,b,c: f'r{c} = r{a}', 
        'seti': lambda a,b,c: f'r{c} = {a}', 
        'gtir': lambda a,b,c: f'r{c} = {a} > r{b} ? 1 : 0', 
        'gtri': lambda a,b,c: f'r{c} = r{a} > {b} ? 1 : 0', 
        'gtrr': lambda a,b,c: f'r{c} = r{a} > r{b} ? 1 : 0', 
        'eqir': lambda a,b,c: f'r{c} = {a} == r{b} ? 1 : 0', 
        'eqri': lambda a,b,c: f'r{c} = r{a} == {b} ? 1 : 0', 
        'eqrr': lambda a,b,c: f'r{c} = r{a} == r{b} ? 1 : 0',
    }

    ip, instructions = data(full=True)
    divider = ('====='*5) + '\n'
    print('IP:', ip)
    print('IS:', len(instructions))
    for i, instruction in enumerate(instructions):
        cmd, a, b, c = instruction
        idx = str(i).ljust(4)
        code = display[cmd](a,b,c)
        print(idx, code)
    print(divider)

    reg: list[int] = [1,0,0,0,0,0]
    count: dict[int,int] = defaultdict(int)
    limit = len(instructions)
    
    while True:
        idx = reg[ip]
        count[idx] += 1
        stop = count[idx] == 4
        instruction = instructions[idx]
        cmd, a, b, c = instruction
        print('Idx :', idx)
        print('Rep :', count[idx])
        print('Raw :', '%s %d %d %d' % instruction)
        print('Cmd :', display[cmd](a,b,c))
        print('Pre :', reg)
        execute(instruction, reg)
        print('Post:', reg)
        idx = reg[ip] + 1 
        if 0 <= idx < limit:
            reg[ip] = idx 
        else:
            break 
        if stop: 
            break

        print('Inc :', reg)
        print(divider)

if __name__ == '__main__':
    do(solve, 18, 19)
    # analyzeProgram()

'''
Part1:
- Run the instructions, with the 6 registers starting at 0
- Execution of commands is similar to 1816 
- The instruction pointer is stored in one of the registers, indicated by ip index
- Get the instruction index from the register[ip]; run this instruction 
- Increment the value of register[ip]; if still within bounds (0, limit), update register[ip] to this incremented value
- Otherwise, break out of the loop 
- Output the value at register 0 

Part2:
- Analyze the program first, as there are two long loops that stall the program execution for a long time
- From the analysis of the program execution: 
    - From 0, jump straight to instruction 17
    - 17 to 35 computes the big number target (N) and stores in r2
    - 35 jumps back to 1 which initializes the r1 (factor) to 1
    - Idx 2 resets the r3 (counter) to 1 
    - 3 to 11 forms the inner-loop:
        - Idea: find the value for r3 which makes r3 * r1 (factor) == r2 (big number)
        - There is only 1 number, if any, that will make this true 
        - This checking happens at idx 4 command
        - The inner loop goes from 1 up to big number to find the r3 value which makes it true
        - Summary: inner-loop is checking if r1 is a factor of the big number:
          is there a number between 1 to N that will become the clean quotient of N / r1 (factor)
        - If we find an r3 which makes r3 * r1 == r2, we go to Idx 7
        - Reaching Idx7 means current r1 is a factor of N, so we increment r0 (the total) by r1 (the factor)
        - Otherwise, we just increment r1 until we exceed r2 (no need to do this, we know nothing else will make the idx 4 comparison true)
    - After exiting the inner loop by making r3 exceed r2 (N), we reach idx 12 
    - 12 to 15 forms the outer-loop:
        - Idx 12 increments r1 => we move to the next factor (start at 1, 2, ...)
        - Idx 13 checks if r1 (factor) has exceeded r2 (big number) 
        - Exit the outer loop if factor has exceeded the big number (goes to 16 = exit)
        - Otherwise, we loop back to instruction 2, which then enters the inner loop
- In other test cases, the registers of interest are in different indexes, so run analyzeProgram 
  to find the instruction index to break the loop and the register index to find the target number
- Summary: the program is trying to find the sum of the factors of N 
    - Outer loop: Incrementing the value for r1 (factor), from 1 to N (big number)
    - Inner loop: trying to find a value for r3 which makes r1 * r3 == r2 (N)
    - The inner loop could be avoided because there's only 1 value for this if ever 
    - The inner loop is deciding whether r1 is a factor of r2 or not (cleanly divides)
    - If it is, we add r1 to r0, which holds the total (and eventually is the output)
- Shortcut: once we find the command that starts the inner loop, we can just simulate the program:
    - Find the sum of numbers from 1 to N, that is a factor (cleanly divides) N
'''