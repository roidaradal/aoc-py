# Advent of Code 2020 Day 08
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[strInt]:
    def fn(line: str) -> strInt:
        p = line.split()
        return p[0], int(p[1])
    return [fn(line) for line in readLines(20, 8, full)]

def part1():
    codes = data(full=True) 
    value, _ = runCodes(codes)
    print(value)

def part2():
    codes = data(full=True)
    for i,(cmd,_) in enumerate(codes):
        if cmd == 'acc': continue # skip, not corrupted
        codes2 = flipNopJmp(codes, i)
        value, stuck = runCodes(codes2)
        if not stuck:
            print(value)
            return 

def runCodes(codes: list[strInt]) -> tuple[int, bool]:
    i, x = 0, 0 
    done = set()
    numCodes = len(codes)
    while True:
        if i in done:
            return x, True 
        if i >= numCodes:
            return x, False 
        
        done.add(i)
        cmd, y = codes[i]
        if cmd == 'nop':
            i += 1 
        elif cmd == 'acc':
            x += y 
            i += 1
        elif cmd == 'jmp':
            i += y

def flipNopJmp(codes: list[strInt], idx: int) -> list[strInt]:
    codes2 = codes[:]
    cmd, y = codes2[idx]
    cmd2 = 'nop' if cmd == 'jmp' else 'jmp'
    codes2[idx] = (cmd2, y)
    return codes2

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Run the codes and print the accumulator value

Part2:
- For nop and jmp commands, try to flip them to the opposite 
- Skip checking acc commands as they are not corrupted 
- Create a copy of the codes where the current nop/jmp command is flipped 
- Run the updated codes and check if it ended while stuck on a loop
- If not stuck on a loop, print the accumulator value

RunCodes:
- Start at index = 0 and value = 0 
- Keep track of index of done codes (for loop checking)
- If we go back to an already done index, stuck in loop so return current value and True (stuck)
- If we have finished processing all codes, return current value and False (not stuck)
- For nop commands, just increment the index by 1 
- For acc commands, increase the value by the parameter and increment index by 1 
- For jmp commands, increase the index by the parameter
'''