# Advent of Code 2019 Day 02
# John Roy Daradal 

import itertools
from aoc import *

def data(full: bool) -> list[int]:
    line = readLines(19, 2, full)[0]
    return toIntList(line, ',')

def part1():
    numbers = data(full=True)
    numbers[1] = 12
    numbers[2] = 2 
    output = runProgram(numbers)
    print(output)

def part2():
    numbers = data(full=True)
    goal =  19690720 
    for (noun,verb) in itertools.product(range(100), repeat=2):
        memory = numbers[:]
        memory[1] = noun 
        memory[2] = verb 
        if runProgram(memory) == goal:
            print((100*noun) + verb)
            return

def runProgram(numbers: list[int]) -> int: 
    i = 0 
    while True:
        cmd = numbers[i]
        if cmd == 99: break 
        in1, in2, out = numbers[i+1:i+4]
        if cmd == 1:
            numbers[out] = numbers[in1] + numbers[in2]
        elif cmd == 2:
            numbers[out] = numbers[in1] * numbers[in2]
        i += 4 
    return numbers[0]

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Set numbers[1] = 12, numbers[2] = 2, as instructed 
- Run program and print the output (numbers[0])

Part2:
- Check all pairs from 0 to 99, set their value to numbers[1], numbers[2]
- Run program for all pairs until we find the goal output

RunProgram:
- if cmd is 99: stop 
- else, e next 3 digits indicate the index for input1, input2, output 
- if cmd == 1, add the numbers found in index=input1, input2 and store to index=output 
- if cmd == 2: same as cmd1, but multiply 
- move ahead 4 spots (1 for cmd, 3 for the parameters)
- Return the output value (numbers[0])
'''