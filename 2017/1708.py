# Advent of Code 2017 Day 08
# John Roy Daradal 

import operator
from aoc import *

T = {
	'=='	: operator.eq,
	'!='	: operator.ne,
	'>'		: operator.gt, 
	'>='	: operator.ge,
	'<'		: operator.lt,
	'<='	: operator.le,
}

class Instruction:
    def __init__(self, line: str):
        head, tail = splitStr(line, ' if ')
        reg, op, val = head.split()
        factor = -1 if op == 'dec' else 1
        self.targetReg = reg 
        self.inc = int(val) * factor
        reg, op, val = tail.split()
        self.condReg = reg 
        self.fn = T[op]
        self.value = int(val)
    
    def isSatisfied(self, value: int) -> bool:
        return self.fn(value, self.value)

def data(full: bool) -> list[Instruction]:
    return [Instruction(line) for line in readLines(17, 8, full)]

def solve() -> Solution:
    instructions = data(full=True)
    reg = defaultdict(int)
    maxVal = 0
    for cmd in instructions:
        if cmd.isSatisfied(reg[cmd.condReg]):
            reg[cmd.targetReg] += cmd.inc
            # Part 2
            maxVal = max(maxVal, reg[cmd.targetReg])
    # Part 1 
    maxReg = max(reg.values())
    return newSolution(maxReg, maxVal)

if __name__ == '__main__':
    do(solve, 17, 8)

'''
Solve:
- Process instructions to fill in register values
- Use defaultdict for register, default value = 0
- Get the condition register's value, use that to check if condition is satisfied
- If satisfied, update the target register using the increment
- Use a mapping of operators to their operator function for dynamic operators
- For part 1, output the maximum register value after processing the instructions
- For part 2, output the maximum register value held by any register at any point during procesing
'''