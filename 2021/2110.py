# Advent of Code 2021 Day 10
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[str]:
    return readLines(21, 10, full)

def part1():
    lines = data(full=True)
    score = {
        ')' : 3,
        ']' : 57,
        '}' : 1197,
        '>' : 25137,
    }
    def illegalScore(line: str) -> int:
        illegal = findIllegal(line)
        return 0 if illegal is None else score[illegal]
    total = getTotal(lines, illegalScore)
    print(total)

def part2():
    lines = data(full=True) 
    score = {
        ')' : 1,
        ']' : 2,
        '}' : 3,
        '>' : 4,
    }
    scores = []
    for line in lines:
        incomplete = findIncomplete(line)
        if incomplete != None:
            scores.append(computeScore(incomplete, score))
    scores.sort()
    mid = len(scores) // 2 
    print(scores[mid])

closer = {
    ')' : '(',
    ']' : '[',
    '}' : '{',
    '>' : '<',
}

opener = {
    '(' : ')',
    '[' : ']',
    '{' : '}',
    '<' : '>',
}

def findIllegal(line: str) -> str|None:
    stack: list[str] = []
    for x in line:
        if x in closer:
            y = stack.pop()
            if y != closer[x]:
                return x
        else:
            stack.append(x)
    return None

def findIncomplete(line: str) -> str|None:
    stack: list[str] = []
    for x in line:
        if x in closer:
            y = stack.pop()
            if y != closer[x]:
                return None # illegal
        else:
            stack.append(x)
    mirror = [opener[x] for x in reversed(stack)]
    return ''.join(mirror)

def computeScore(text: str, score: dict[str,int]) -> int:
    total = 0
    for x in text:
        total = (total * 5) + score[x]
    return total

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Find the first illegal character in each line (open/close nesting doesnt match)
- Go through each character in line; if opener, push to stack 
- If closer, pop off the opener from the stack and check if they match
- Get the total score for the found illegal characters (use the score map)

Part2:
- Skip lines that have illegal characters; only find incomplete lines
- Similar to processing in Part 1, but if illegal character is found (not match), return None (to skip)
- If finished processing line without illegal characters, the remaining characters in the stack
  in reverse order are the closers; get their corresponding openers to form the text that will complete it
- Compute the score of the completion text using the formula (total * 5 + score[char])
- Sort the scores and output the middle score
'''