# Advent of Code 2021 Day 18
# John Roy Daradal 

import json, re
from aoc import *

def data(full: bool) -> list[str]:
    return readLines(21, 18, full)

def solve() -> Solution:
    lines = data(full=True)

    # Part 1
    line1 = lines[0]
    for line2 in lines[1:]:
        line1 = tryReduce(addNumbers(line1, line2))
    total = computeMagnitude(line1)

    # Part 2
    maxMagnitude = 0 
    for i, line1 in enumerate(lines):
        for j, line2 in enumerate(lines):
            if i == j: continue 
            magnitude = computeMagnitude(tryReduce(addNumbers(line1, line2)))
            maxMagnitude = max(maxMagnitude, magnitude)

    return newSolution(total, maxMagnitude)

def tryReduce(line: str) -> str:
    line = line[1:-1] # remove outer brackets

    # Rule 1: Explode leftmost depth-4 pairs
    i, limit = 0, len(line)
    depth = 0
    while i < limit:
        if line[i] == '[':
            depth += 1
        elif line[i] == ']':
            depth -= 1
        if depth == 4:
            idx = findCloser(line, i, '[', ']')
            lval, rval = extractPair(line[i:idx+1])
            # Replace pair with ? for now
            line = '%s?%s' % (line[:i], line[idx+1:])
            # Add lval to next left number
            left = findNumberLeft(line, i-1)
            if left != None:
                start, end = left 
                lval += int(line[start:end])
                line = '%s%d%s' % (line[:start], lval, line[end:])
            # Add rval to next right number 
            right = findNumberRight(line, line.index('?') + 1)
            if right != None:
                start, end = right 
                rval += int(line[start:end])
                line = '%s%d%s' % (line[:start], rval, line[end:])
            # Replace ? with 0 
            line = line.replace('?', '0')
            line = '[%s]' % line # wrap back in brackets 
            return tryReduce(line)
        i += 1

    # Rule 2: 
    number = r'[0-9]+'
    for m in re.finditer(number, line):
        x = int(m.group(0))
        if x >= 10: # found double digit 
            a = x // 2 
            b = x - a 
            pair = '[%d,%d]' % (a, b)
            start, end = m.span()
            line = '[%s%s%s]' % (line[:start], pair, line[end:])
            return tryReduce(line)
        
    # Wrap back in brackets
    line = '[%s]' % line
    return line

def extractPair(line: str) -> int2:
    line = line.strip('[]')
    return toInt2(line, ',')

def addNumbers(line1: str, line2: str) -> str:
    return '[%s,%s]' % (line1, line2)

def findNumberLeft(line: str, start: int) -> int2|None:
    i = start 
    end, start = -1, 0 
    while i >= 0:
        if line[i].isdigit() and end == -1:
            end = i+1 
        elif line[i] == ',' or line[i] == '[':
            if end != -1:
                start = i+1
                break
        i -= 1
    if end == -1:
        return None 
    else:
        return (start, end)
    
def findNumberRight(line: str, start: int) -> int2|None:
    i, limit = start, len(line)
    start, end = -1, limit 
    while i < limit:
        if line[i].isdigit() and start == -1:
            start = i 
        elif line[i] == ',' or line[i] == ']':
            if start != -1:
                end = i 
                break 
        i += 1 
    if start == -1:
        return None 
    else:
        return (start, end)

def computeMagnitude(line: str) -> int:
    items = json.loads(line)
    left, right = items
    lval = 3
    if type(left) == list:
        lval *= computeMagnitude(str(left))
    elif type(left) == int:
        lval *= left 
    rval = 2 
    if type(right) == list:
        rval *= computeMagnitude(str(right))
    elif type(right) == int:
        rval *= right 
    return lval + rval

if __name__ == '__main__':
    do(solve, 21, 18)

'''
Part1:
- Add the first two lines by making them a pair and reducing the result 
- To add line1 and line2, combine them into a new pair: [line1, line2]
- The resulting number is added to the next number and the process is repeated until all lines are processed
- To reduce a line, first remove the outer brackets []
- Rule 1: Explode the leftmost depth-4 pairs:
    - Check if there are any depth-4 pair, by going through the line
    - Seeing a [ increments the depth, while seeing a ] decrements it 
    - If we reach depth 4, find the grouping of that pair by using findCloser
    - An exploding pair will always have 2 numbers inside, so we get the lval and rval
    - Replace the exploding pair in the line with ?, for now (for easy search later)
    - Find a number to the left of the pair and add lval to it, if one is found
    - Find a number to the right of the pair and add rval to it, if one is found 
    - Finally, replace the ? with a 0 and wrap the line back in brackets
    - Recursively call tryReduce on the resulting line, as the new changes might have broken other rules
- Rule 2: Split double-digit numbers
    - Use regex to find number patterns in the line 
    - Go through the numbers from left to right; if one number is double digit, split it
    - Lval is half of the number, while rval is the remaining balance  (e.g. 11 => 5,6, 12 => 6,6)
    - Replace the double digit number with [lval, rval] and wrap the line back in brackets
    - Recursively call tryReduce on the resulting line, as the new changes might have broken other rules
- If we have passed the two rules above, wrap the line back in brackets and return it: it is now valid
- Compute the magnitude of the resulting line
    - Return (3 * leftValue) + (2 * rightValue)
    - If the left/right value is a number, that is the value 
    - Otherwise, if it is a list, recursively call computeMagnitude on it to compute the value

Part2:
- For each pair of line in the input, add the numbers, reduce the result and compute the magnitude
- Return the maximum magnitude out of the computed pair results
'''