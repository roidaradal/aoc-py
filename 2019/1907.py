# Advent of Code 2019 Day 07
# John Roy Daradal 

import itertools
from aoc import *
from intcode import *

def data(full: bool) -> list[int]:
    line = readFirstLine(19, 7, full)
    return toIntList(line, ',')

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    numbers = data(full=True)
    N = 5 
    maxOutput = 0
    for settings in itertools.permutations(range(N), N):
        output: int|None = 0
        for i in range(N):
            inputs = [settings[i]]
            if output != None: inputs.append(output)
            output, _ = runProgram(numbers[:], inputs, 0)
        if output != None:
            maxOutput = max(maxOutput, output)
    return maxOutput

def part2() -> int:
    numbers = data(full=True)
    N = 5 
    maxOutput = 0 
    for settings in itertools.permutations(range(5,10), N):
        program = [numbers[:] for _ in range(N)]
        index = [0 for _ in range(N)]
        stop = [False for _ in range(N)]
        outputs: list[int|None] = [None for _ in range(N)]
        inputs = [[settings[i]] for i in range(N)]
        inputs[0].append(0)
        p = 0
        while not all(stop):
            output, idx = runProgram(program[p], inputs[p], index[p])
            index[p] = idx 
            stop[p] = output is None 
            if output != None: outputs[p] = output
            p = (p+1) % N 
            if output != None: inputs[p].append(output)
        if outputs[-1] != None:
            maxOutput = max(maxOutput, outputs[-1])
    return maxOutput

def runProgram(numbers: list[int], inputs: list[int], start: int) -> tuple[int|None, int]:
    i = start 
    while True:
        word = str(numbers[i])
        head, tail = word[:-2], word[-2:]
        cmd = int(tail)
        if cmd == 99: break 

        if cmd in (1,2,7,8): # Add, Multiply, LessThan, Equals
            in1, in2, out = numbers[i+1:i+4]
            m1, m2, _ = modes(head, 3)
            a = param(in1, m1, numbers)
            b = param(in2, m2, numbers)
            if cmd == 1:
                numbers[out] = a + b
            elif cmd == 2:
                numbers[out] = a * b
            elif cmd == 7: 
                numbers[out] = 1 if a < b else 0
            elif cmd == 8:
                numbers[out] = 1 if a == b else 0
            i += 4
        elif cmd == 3: # Input
            idx = numbers[i+1]
            numbers[idx] = inputs.pop(0)
            i += 2
        elif cmd == 4: # Output
            m = modes(head, 1)[0]
            out = param(numbers[i+1], m, numbers)
            i += 2 
            return (out, i)
        elif cmd == 5 or cmd == 6: #Jump-if-True/False
            p1, p2 = numbers[i+1], numbers[i+2]
            m1, m2 = modes(head, 2)
            isZero = param(p1, m1, numbers) == 0
            doJump = isZero if cmd == 6 else (not isZero)
            if doJump:
                i = param(p2, m2, numbers)
            else:
                i += 3

    return (None,i)

if __name__ == '__main__':
    do(solve, 19, 7)

'''
Part1:
- Try out different permutations of 0 to 4 to use as phase settings for the 5 amplifiers
- Run the intcode program using these settings and get the output 
- Print the max output from running all permutations 

Part2:
- Try out different permutations of 5 to 9 to use as phase settings for the 5 amplifiers
- For each amplifier, keep track of own program, own curent index, if it's stopped, its inputs and outputs
- Initialize all amp's index = 0, stop = False, None as output, inputs = phase setting 
- Add 0 as another input to first amplifier 
- Go through each amplifier in order, looping back when necessary 
- Run the amplifier's program using its current inputs and starting at its index
- After stopping, remember which index it stopped at to resume later 
- Set amplifier to stop if output is None (reached the 99 command)
- Update the amplifier's output if not None 
- Move to next amplifier, and use the previous output and add it to the next amp's input
- Stop if all amplifiers have halted
- For this phase setting, the output is the last amplifier's output
- Print the max output from running all permutations

RunProgram:
- Similar to RunProgram in 1905
- Can start at specific index, since program can be resumed from previous run
- For inputs, a list of input numbers is provided 
- For output, we return the output number
'''