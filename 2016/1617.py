# Advent of Code 2016 Day 17
# John Roy Daradal 

from aoc import *

bounds: dims2  = (4, 4)
goal  : coords = (3, 3)

def data(full: bool) -> str:
    return readFirstLine(16, 17, full)

def solve() -> Solution:
    passcode = data(full=True)

    # Part 1 
    minPath = bfsFindVault(passcode, True)

    # Part 2 
    maxPath = bfsFindVault(passcode, False)
    maxSteps = len(maxPath)

    return newSolution(minPath, maxSteps)

def bfsFindVault(passcode: str, findMin: bool) -> str:
    curr: coords = (0,0)
    q: list[tuple[coords,str]] = [(curr, "")]
    maxPath = ""
    while len(q) > 0:
        curr, path = q.pop(0)
        if curr == goal:
            if findMin:
                return path 
            elif len(path) > len(maxPath):
                maxPath = path
            continue
        hash = md5Hash(passcode+path)[:4]
        for step, nxt in getMoves(hash, curr).items():
            q.append((nxt, path+step))
    return "" if findMin else maxPath

def getMoves(hash: str, curr: coords) -> dict[str, coords]:
    moves = [('U',U), ('D', D), ('L', L), ('R', R)]
    valid: dict[str, coords] = {}
    for i,h in enumerate(hash):
        if h not in 'bcdef': continue # skip closed
        step, d = moves[i]
        nxt = move(curr, d)
        if not insideBounds(nxt, bounds): continue
        valid[step] = nxt
    return valid

if __name__ == '__main__':
    do(solve, 16, 17)

'''
Solve:
- Use BFS to find the vault at (3,3)
- For Part 1, find the minimum path to reach the vault 
- For Part 2, find the maximum path length to reach the vault 
- Start at (0, 0) with empty steps 
- During BFS, once we find the goal coordinates:
    - If finding the minimum path, return path right away 
    - If finding the maximum path, compare with current maxPath
- To get the next steps, get the MD5 Hash of the passcode + current path
- Use the first 4 characters of the resulting hash (hex):
    - They represent the doors UDLR 
    - Only bcdef = open door; skip moves that are closed and out of bounds
- Add to the queue the next coords and the resulting path: existing + next step
'''