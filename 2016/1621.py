# Advent of Code 2016 Day 2
# John Roy Daradal 

from aoc import *

LEFT, RIGHT = -1, 1

class Operation:
    def __init__(self, kind: str, useNum: bool, num1: int=0, num2: int=0, char1: str='', char2: str=''):
        self.kind = kind 
        self.useNum = useNum 
        self.num1 = num1 
        self.num2 = num2 
        self.char1 = char1 
        self.char2 = char2 
    
    def apply(self, code: list[str], reverse: bool=False) -> list[str]:
        limit = len(code)
        if self.kind == 'swap' and self.useNum:
            # swap position
            idx1, idx2 = self.num1, self.num2 
            code[idx1], code[idx2] = code[idx2], code[idx1]
        elif self.kind == 'swap' and not self.useNum:
            # swap letter 
            idx1, idx2 = code.index(self.char1), code.index(self.char2)
            code[idx1], code[idx2] = code[idx2], code[idx1]
        elif self.kind == 'rotate' and self.useNum:
            # rotate left/right 
            direction, steps = self.num1, self.num2 
            steps = steps % limit
            reverseLeft = (direction == LEFT and not reverse) or (direction == RIGHT and reverse)
            if reverseLeft:
                code = code[steps:] + code[:steps]
            else:
                code = code[-steps:] + code[:-steps]
        elif self.kind == 'rotate' and not self.useNum:
            # rotate based on letter 
            if reverse:
                for idx in range(limit):
                    # Try 0 to 3
                    if idx < 4:
                        steps = 1 + idx
                        code2 = code[steps:] + code[:steps]
                        if code2.index(self.char1) == idx:
                            code = code2
                            break
                    # Try 4 onwards 
                    idx2 = 4+idx
                    if idx2 < limit:
                        steps = (1 + idx2 + 1) % limit 
                        code2 = code[steps:] + code[:steps]
                        if code2.index(self.char1) == idx2:
                            code = code2 
                            break                
            else:
                idx = code.index(self.char1)
                extra = 1 if idx >= 4 else 0 
                steps = (1 + idx + extra) % limit
                code = code[-steps:] + code[:-steps]
        elif self.kind == 'reverse':
            # reverse
            idx1, idx2 = self.num1, self.num2 
            code = code[:idx1] + code[idx1:idx2][::-1] + code[idx2:]
        elif self.kind == 'move':
            # move 
            idx1, idx2 = self.num1, self.num2 
            if reverse:
                item = code[idx2]
                code.remove(item)
                code.insert(idx1, item) 
            else:
                item = code[idx1]
                code.remove(item)
                code.insert(idx2, item)

        return code

def data(full: bool) -> list[Operation]:
    def fn(line: str) -> Operation:
        parts = splitStr(line, None)
        kind, useNum = '', False
        num1, num2 = 0, 0
        char1, char2 = '', ''
        if line.startswith('swap position'):
            kind = 'swap'
            useNum = True
            num1, num2 = int(parts[2]), int(parts[-1])
        elif line.startswith('swap letter'):
            kind = 'swap'
            useNum = False 
            char1, char2 = parts[2], parts[-1]
        elif line.startswith('rotate based'):
            kind = 'rotate'
            useNum = False 
            char1 = parts[-1]
        elif line.startswith('rotate'):
            kind = 'rotate'
            useNum = True 
            num1 = LEFT if parts[1] == 'left' else RIGHT 
            num2 = int(parts[2])
        elif line.startswith('reverse'):
            kind = 'reverse'
            useNum = True 
            num1, num2 = int(parts[2]), int(parts[-1])+1
        elif line.startswith('move'):
            kind = 'move'
            useNum = True 
            num1, num2 = int(parts[2]), int(parts[-1])
        return Operation(kind, useNum, num1, num2, char1, char2)


    return [fn(line) for line in readLines(16, 21, full)]

def solve() -> Solution:
    operations = data(full=True)

    # Part 1
    code = list('abcdefgh')
    for operation in operations:
        code = operation.apply(code)
    code1 = ''.join(code)

    # Part 2 
    code = list('fbgdceah') 
    for operation in reversed(operations):
        code = operation.apply(code, reverse=True)
    code2 = ''.join(code)

    return newSolution(code1, code2)

if __name__ == '__main__':
    do(solve, 16, 21)

'''
Part1:
- Starting with the input code, apply the operations in order to produce the encrypted code:
- Swap position: swap the letters at idx1 and idx2
- Swap letters : find char1 and char2 and swap them
- Rotate left  X steps: take the first X chars and put them at the back (maintain order)
- Rotate right X steps: take the last X chars and put them in front (maintain order)
- Reverse idx1 to idx2: combine the prefix, the reversed subpart, and the suffix
- Move idx1 -> idx2: remove the item at idx1, and re-insert it before idx2
- Rotate based on letter: find index of char1; extra step = 1 if idx >= 4, 
  then rotate right for steps = (1 + idx + extra) % len(code)

Part2:
- Given the encrypted code, reverse the process to get the original input
- Go through the operations in reverse order
- Apply the reverse operation on the current code:
- Swap position, swap letters, reverse subpart are the same in reverse order
- Rotate left/right: reverse the direction
- Move idx2 -> idx1: remove the item at idx2, and re-insert it before idx1
- Rotate based on letter: we don't know the prior index of char1 so we will try the different possibilities:
    - Try index from 0 to limit, but try both the 0-3 and 4-onwards in parallel
    - If index 0 to 3, steps = 1 + idx (no extra), then rotate left
    - If index 4 onwards, steps = (1 + idx + 1) % limit, then rotate left 
    - If resulting code's index of char1 is the current index, we have found the prior inde of char1, stop the loop
'''