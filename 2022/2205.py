# Advent of Code 2022 Day 05
# John Roy Daradal 

from aoc import *

cmd = tuple[int,int,int]

def data(full: bool) -> tuple[list[list[str]], list[cmd]]:
    stacks, moves = [], []
    stackMode = True
    for line in readLines(22, 5, full, strip=False):
        clean = line.strip()
        if clean == '':
            stackMode = False 
            continue 
        if stackMode:
            if not clean.startswith('['): 
                continue # skip stack numbers
            if len(stacks) == 0:
                count = len(line) // 4 # each stack has 4 chars
                stacks = [[] for _ in range(count)]
            for i,char in enumerate(line):
                if i % 4 != 1 or char == ' ': # 2nd char of each stack column is the value
                    continue                  # skip other chars and blanks
                idx = i // 4 
                stacks[idx].append(char)
        else:
            p = splitStr(line, None)
            count = int(p[1])
            src, dst = int(p[3])-1, int(p[5])-1
            moves.append((count, src, dst))
    return stacks, moves

def solve() -> Solution:
    # Part 1
    stacks, moves = data(full=True)
    top1 = processMoves(stacks, moves, True)

    # Part 2 
    stacks, moves = data(full=True)
    top2 = processMoves(stacks, moves, False)

    return newSolution(top1, top2)

def processMoves(stacks: list[list[str]], moves: list[cmd], reverse: bool) -> str:
    for count, idx1, idx2 in moves:
        transfer(stacks, count, idx1, idx2, reverse)
    return ''.join(s[0] for s in stacks)

def transfer(stacks: list[list[str]], count: int, idx1: int, idx2: int, reverse: bool):
    s1, s2 = stacks[idx1], stacks[idx2]
    move = s1[:count]                           # get the top count items
    move = move[::-1] if reverse else move[:]   # reverse / copy
    move.extend(s2)                             # move list becomes the top of stack of s2
    stacks[idx1] = s1[count:]
    stacks[idx2] = move

if __name__ == '__main__':
    do(solve, 22, 5)

'''
ProcessMoves:
- Stack is stored where top is at index 0 in the list
- Process each move (count, idx1, idx2) in order
- Transfer count items from stack in idx1 to idx2 
- Return the top items in each stack to form the output message

Transfer:
- Moved chunk is the top count items of stack1 
- In Part1, reverse the moved chunk when transferring
- In Part2, transfer the moved chunk as is
- Add this moved chunk to top of stack 2 
- Update stack 1, remove the moved chunk
'''