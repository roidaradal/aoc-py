# Advent of Code 2018 Day 21
# John Roy Daradal 

from aoc import *

Instruction = tuple[str, int, int, int]

def data(full: bool) -> tuple[int, list[Instruction]]:
    ip: int = 0 
    instructions: list[Instruction] = []
    for line in readLines(18, 21, full):
        if line.startswith('#ip'):
            ip = int(line.split()[1])
        else:
            cmd, a, b, c = splitStr(line, None)
            instructions.append((cmd, int(a), int(b), int(c)))
    return ip, instructions

def solve() -> Solution:
    _, instructions = data(full=True)
    initialR4 = instructions[7][1]

    # Part 1
    r3 = 65536 
    minR0 = solveR0(r3, initialR4)

    # Part 2
    done: list[int] = [minR0]
    r4 = minR0
    while True:
        r3 = r4 | 65536
        r4 = solveR0(r3, initialR4)
        if r4 in done: break
        done.append(r4)
    maxR0 = done[-1]

    return newSolution(minR0, maxR0)

def solveR0(r3: int, initialR4: int) -> int:
    r4 = initialR4
    while True:
        r4 += r3 & 255 
        r4 &= 16777215
        r4 *= 65899
        r4 &= 16777215
        
        if 256 > r3: 
            break
        else:
            r3 //= 256
    return r4

if __name__ == '__main__':
    do(solve, 18, 21)

'''
Solve: 
- For Part 1, find the minimum value for R0 that will make the program halt after executing the fewest instructions
    - Only need one iteration of the main loop, and exit right away = halted after fewest instructions
    - Start with r3 = 65536, from commands 5-6 r3 = 0|65536 = 65536
- For Part 2, find the minimum value for R0 that will make the program halt after executing the most instructions
    - We need to detect a loop in the output R0 values and stop before we reach the loop, so that the program 
      can halt, and this is the most number of instructions it can do, before entering an infinite loop
    - Start with the r0 from Part 1, then update r3 = r4 | 65536 (command 6) inside the loop
    - The r0 from solveR0 will also become the next r4 in the next iteration; if this has already been seen before,
      we break out of the loop, as this will introduce an infinite loop; the maxR0 is the previous R0 before seeing the loop

SolveR0:
- Manually analyzed the input data; only the value at instructions[7] varies = the initial value of R4
- Manually analyzed the program flow: it boils down to the ff:
    - r4 = (((r4 + (r3 & 255)) & 16777215) * 65899) & 16777215
    - if r3 <= 256, stop the loop and return the r4 value above 
    - Otherwise, divide r3 by 256
- 0-4: prelude that does nothing (123 & 456 == 72, always true)
- 5: initial r4 = 0
- 6: r3 = r4|65536 (start of the loop)
- 7: r4 = inital r4 value (the variable for each input data)
- 8-12: sets up the equation for r4 above
- 13-16: checks for stopping condition: 256 > r3, if not yet satisfied, continue below; otherwise skip all the way to 28
- 17-26: divides r3 by 256
- 27: loop back to 8, continuing the loop
- 28: check if r4 == r0, exit => to make the loop exit faster, need r0 value equal r4
- 29-30: loop back to 6 (continue the main loop)
'''