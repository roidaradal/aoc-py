# Advent of Code 2016 Day 07
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[str]:
    return readLines(16, 7, full)

def part1():
    words = data(full=True)
    count = countValid(words, isValid)
    print(count)

def part2():
    words = data(full=True)
    count = countValid(words, isValid2)
    print(count)

def isValid(word: str) -> bool:
    found = False
    flip = False 
    for i in range(len(word)-3):
        if word[i] == '[':
            flip = True
        elif word[i] == ']':
            flip = False
        elif isABBA(word[i:i+4]):
            if flip: return False # found inside brackets
            found = True
    return found

def isValid2(word: str) -> bool:
    look, found = set(), set()
    flip = False 
    for i in range(len(word)-2):
        sub = word[i:i+3]
        if word[i] == '[':
            flip = True
        elif word[i] == ']':
            flip = False 
        elif isABA(sub):
            if flip:
                found.add(toABA(sub))
            else:
                look.add(sub)
    common = look.intersection(found)
    return len(common) > 0

def isABBA(word: str) -> bool:
    if len(word) != 4: return False
    ok1 = word[0] != word[1]
    ok2 = word[0:2][::-1] == word[2:]
    return ok1 and ok2

def isABA(word: str) -> bool:
    if len(word) != 3: return False
    ok1 = word[0] != word[1]
    ok2 = word[0] == word[2]
    return ok1 and ok2

def toABA(bab: str) -> str:
    b,a = bab[0],bab[1]
    return a+b+a

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Valid word if we find an ABBA substring but not inside square brackets
- When we encounter [ and ], turn on / off the flip flag, respectively
- If we find ABBA pattern but flip is on, then it is invalid

Part2:
- Valid word if we find an ABA substring outside brackets with a corresponding BAB inside brackets
- Toggle the flip flag on/off with [ and ], similar to Part 1
- If we find an ABA substring outside brackets, add this to set of ABA to look for
- If we find a BAB substring inside brackets, add its ABA version to set of ABA found
- Check if the set to look for and the set of found ABAs have something in common
'''