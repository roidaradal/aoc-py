# Advent of Code 2018 Day 16
# John Roy Daradal 

from aoc import *

Register = tuple[int,int,int,int]
Instruction = tuple[int,int,int,int]
Sample = tuple[Instruction,Register,Register]

opcodes = [
    'addr', 'addi',
    'mulr', 'muli',
    'banr', 'bani',
    'borr', 'bori',
    'setr', 'seti',
    'gtir', 'gtri', 'gtrr',
    'eqir', 'eqri', 'eqrr',
]

def data(full: bool) -> tuple[list[Sample], list[Instruction]]:
    before: Register|None = None
    after:  Register|None = None
    instruction: Instruction|None = None
    space = 0
    samples: list[Sample] = []
    instructions: list[Instruction] = []
    instructionMode = False
    for line in readLines(18, 16, full):
        if line == '':
            space += 1
            if before != None and after != None and instruction != None: 
                samples.append((instruction, before, after))
                before, after, instruction = None, None, None
        elif line.startswith('Before:'):
            tail = splitStr(line, ':')[1].strip('[]')
            a,b,c,d = toIntList(tail, ',')
            before = (a,b,c,d)
            space = 0
        elif line.startswith('After:'):
            tail = splitStr(line, ':')[1].strip('[]')
            a,b,c,d = toIntList(tail, ',')
            after = (a,b,c,d)
            space = 0
        else:
            a,b,c,d = toIntList(line, None)
            instruction = (a,b,c,d)
            space = 0
            if instructionMode: instructions.append(instruction)
        if space == 3: instructionMode = True
    return samples, instructions

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    samples, _ = data(full=True)
    count = 0
    for instruction, before, after in samples:
        valid = 0
        for cmd in opcodes:
            result = execute(cmd, before, instruction)
            if result == after:
                valid += 1 
        if valid >= 3:
            count += 1
    return count

def part2() -> int:
    samples, instructions = data(full=True)

    # setup the domain of each opcode
    domain: dict[int,list[str]] = {}
    for i in range(len(opcodes)):
        domain[i] = opcodes[:]  

    # figure out the opcode mapping by narrowing down the domains 
    for instruction, before, after in samples:
        valid: list[str] = []
        opcode = instruction[0]
        for cmd in domain[opcode]:
            result = execute(cmd, before, instruction)
            if result == after:
                valid.append(cmd)
        domain[opcode] = valid

    # finalize the mapping by eliminating sure commands from other domains
    cmdOf: dict[int,str] = {}
    unassigned = list(range(len(opcodes)))
    while len(unassigned) > 0:
        prune: list[str] = []
        assigned: list[int] = []
        for opcode in unassigned:
            if len(domain[opcode]) == 1:
                cmd = domain[opcode][0]
                cmdOf[opcode] = cmd 
                prune.append(cmd)
                assigned.append(opcode)

        for opcode in assigned:
            unassigned.remove(opcode)
        for opcode in unassigned:
            for cmd in prune:
                if cmd not in domain[opcode]: continue
                domain[opcode].remove(cmd)

    # Process instructions 
    register: Register = (0,0,0,0)
    for instruction in instructions:
        opcode = instruction[0]
        register = execute(cmdOf[opcode], register, instruction)

    return register[0]

def execute(cmd: str, register: Register, instruction: Instruction) -> Register:
    reg = list(register)
    _, a, b, c = instruction
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
    r1,r2,r3,r4 = reg 
    return (r1,r2,r3,r4)

if __name__ == '__main__':
    do(solve, 18, 16)

'''
Part1:
- Process each (instruction, before, after) samples from the input data
- Test each sample using the 16 available opcodes, using the instruction and before register
- If the resulting register is the after register, it is valid
- Output the number of samples with valid count >= 3

Part2:
- Figure out the mapping of opcode => cmd by domain reduction and elimination 
- Initialize all domains to all 16 opcodes
- Process the samples similar to Part 1; only the valid cmds remain as the opcode's domain
- This reduces the opcode domains from 16 down to some number; 1 of them will be definite (only 1 left in domain)
- Finalize the mapping by process of elimination: 
    - Starting from the opcode with only 1 cmd in the domain (sure); add this assignment 
      and remove the cmd from other opcode's domains 
    - This creates a ripple effect, making other opcodes become sure as they are reduced to 1 cmd in domain 
    - Repeat the process until we have all opcodes assigned to a cmd
- With the opcode => cmd mapping finalized, process the instructions starting with registers set to 0
- Execute the instructions with the correct cmd and output the register 0 value after processing everything
'''