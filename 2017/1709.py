# Advent of Code 2017 Day 09
# John Roy Daradal 

from aoc import *

def data(full: bool) -> str:
    return readFirstLine(17, 9, full)

def solve() -> Solution:
    stream = data(full=True)
    i, limit = 0, len(stream)
    count, total = 0, 0
    garbage = False
    stack = []
    while i < limit:
        char = stream[i]
        if garbage:
            if char == '!':
                i += 1 # skip next character
            elif char == '>':
                garbage = False
            else:
                count += 1
        elif char == '{':
            score = 1 if len(stack) == 0 else (stack[-1] + 1)
            stack.append(score)
        elif char == '}':
            total += stack.pop()
        elif char == '<':
            garbage = True
        i += 1
    # Part 1 and 2 
    return newSolution(total, count)

if __name__ == '__main__':
    do(solve, 17, 9)

'''
Solve:
- Process each character of the stream
- If char is < this starts the garbage zone
- If in garbage zone, char > closes the garbage, and !x skips the x character
- For Part 1, compute the total score of non-garbage groups
- Outer group has score of 1, while inner group's score is 1 more than the number of groups that encloses it
- Finding char } closes a group, so we remove it from the stack
- For Part 2, count the non-cancelled characters inside the garbage zones
'''