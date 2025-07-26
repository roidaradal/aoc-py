# Advent of Code 2024 Day 17
# John Roy Daradal 

from aoc import *

def data(full: bool) -> tuple[list[int], list[int]]:
    lines = readLines(24, 17, full)
    register: list[int] = []
    for line in lines[0:3]:
        value = splitStr(line, ':')[1]
        register.append(int(value))
    tail = splitStr(lines[4], ':')[1]
    program = toIntList(tail, ',')
    return register, program

def solve() -> Solution:
    register, program = data(full=True)
    
    # Part 1
    output = getProgramOutput(register, program)

    # Part 2
    a = reverseProgram(program, program)

    return newSolution(output, a)

def getProgramOutput(register: list[int], program: list[int]) -> str:
    a,b,c = 0,1,2
    ip, limit = 0, len(program)-1
    output: list[str] = []
    while ip < limit:
        opcode = program[ip]
        operand = program[ip+1]
        jumped = False
        comboValue = combo(operand, register)
        match opcode:
            case 0:
                register[a] //= 2 ** comboValue 
            case 1:
                register[b] ^= operand 
            case 2:
                register[b] = comboValue % 8
            case 3:
                if register[a] != 0:
                    ip = operand
                    jumped = True
            case 4:
                register[b] ^= register[c]
            case 5:
                out = comboValue % 8 
                output.append(str(out))
            case 6:
                register[b] = register[a] // (2 ** comboValue)
            case 7:
                register[c] = register[a] // (2 ** comboValue)
        
        if not jumped: ip += 2

    return ','.join(output)

def combo(x: int, register: list[int]) -> int:
    if 0 <= x <= 3:
        return x
    elif 4 <= x <= 6:
        idx = x-4 
        return register[idx]
    else:
        return 0

def reverseProgram(output: list[int], program: list[int]) -> int:
    revProgram: list[int2] = []
    for i in range(0, len(program), 2):
        revProgram.append((program[i], program[i+1]))
    revProgram = revProgram[::-1]

    aDomain = [0] # program stops if reg[A] is 0
    reg = "abc"
    for round, goal in enumerate(reversed(output)):
        expr = ""
        aRanges: list[int2] = []
        for opcode, operand in revProgram:
            idx = operand-4
            match opcode:
                case 0:
                    # assumption: literal operand
                    factor = 2**operand 
                    for a in aDomain:
                        start = factor * a 
                        end = start + factor 
                        if round == 0 and start == 0:
                            start = 1
                        aRanges.append((start, end))
                case 1:
                    # replace b => (b^operand)
                    expr = expr.replace('b', '(b^%d)' % operand)
                case 2:
                    # replace b => (reg % 8)
                    # assumption: combo operand is register 
                    expr = expr.replace('b', '(%s%%8)' % reg[idx])
                case 3:
                    # ignore checking if reg[A] != 0
                    continue 
                case 4:
                    # replace b => (b^c)
                    expr = expr.replace('b', '(b^c)')
                case 5:
                    # expr starts with the variable of the output register
                    # assumption: combo operand is register, otherwise output is static
                    expr = '%s%%8' % reg[idx]
                case 6:
                    # replace b => a // (2**reg)
                    # assumption: combo operand is register 
                    expr = expr.replace('b', '(a//(2**%s))' % reg[idx])
                case 7:
                    # replace c => a // (2**reg)
                    # assumption: combo operand is register 
                    expr = expr.replace('c', '(a//(2**%s))' % reg[idx])
        
        aDomain = []
        for start,end in aRanges:
            for aCandidate in range(start, end):
                result = evalExpr(expr, aCandidate)
                if result == goal:
                    aDomain.append(aCandidate)

    return min(aDomain)

def evalExpr(expr: str, a: int) -> int:
    expr = expr.replace('a', str(a))
    return int(eval(expr))

if __name__ == '__main__':
    do(solve, 24, 17)

'''
Part1:
- Simulate the program using the initial register values from the input
- Process the program numbers in pairs: opcode, operand
- For combo operands: 0-3 are literal values, 4-6 uses the values at register A,B,C
- OpCode0: reg[A] = reg[A] // (2 ** combo(operand))
- OpCode1: reg[B] = reg[B] ^ operand 
- OpCode2: reg[B] = combo(operand) % 8 
- OpCode3: if reg[A] != 0: ip = operand 
- OpCode4: reg[b] = reg[B] ^ reg[C]
- OpCode5: output => combo(operand) % 8
- OpCode6: reg[B] = reg[A] // (2 ** combo(operand))
- OpCode7: reg[C] = reg[A] // (2 ** combo(operand))
- Return the list of outputs separated by comma

Part2:
- Reverse the process: starting from the output, find out the minimum value of the A register to produce this output
- We feed the program numbers as the intended output
- Since we are working in reverse order, go through the program pairs in reverse order:
  start from the part where it checks whether to continue the loop and where it adds to the output 
- We start with the domain of A being just 0 - since we know the program stops when reg[A] == 0
- Process the outputs in reverse order (last output first)
- For each output, process the reversed program pairs, and build the expression incrementally
- OpCode0: Compute factor = 2**operand; for each a in the aDomain, we create an a-range, 
  where start = factor * a, end = start+factor (except for round 0, cannot start with 0)
- OpCode1: Replace b => (b^operand) in the expr 
- OpCode2: Replace b => (reg%8) in the expr, where reg is the combo operand
- OpCode3: Ignore: this is the check for the jump back to start to continue loop
- OpCode4: Replace b => (b^c) in the expr
- OpCode5: This is the output, so we initialize expr = (reg%8), where reg is the combo operand
- OpCode6: Replace b => (a//2(**reg)), where reg is the combo operand
- OpCode7: Replace c => (a//2**(reg)), where reg is the combo operand
- After processing the outputs, we now have the final expr to evaluate
- From the a-ranges created from OpCode0, check all possible a candidates from that range:
    - Replace the 'a' in expr with the actual a candidate value and use eval() to evaluate the expr
    - If the result of the expr is the current output being processed, we add this candidate to the next aDomain
- After processing all outputs, we return the minimum out of the remaining aDomain 
'''