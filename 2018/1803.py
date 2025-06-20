# Advent of Code 2018 Day 03
# John Roy Daradal 

from aoc import *

claim = tuple[int,coords,dims2]

def data(full: bool) -> list[claim]:
    def fn(line: str) -> claim:
        head, tail = splitStr(line, '@')
        p = splitStr(tail, ':')
        col,row = toIntList(p[0], ',')
        w, h = toIntList(p[1], 'x')
        cid = int(head.strip('#'))
        return (cid, (row,col), (h,w))
    return [fn(line) for line in readLines(18, 3, full)]

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    claims = data(full=True)
    g = createGrid(0, 1000, 1000) 
    for _,start,dims in claims:
        (row,col), (h,w) = start, dims
        for dy in range(h):
            r = row+dy 
            for dx in range(w):
                c = col+dx 
                g[r][c] += 1
    count = sum(sum(1 for x in line if x > 1) for line in g)
    return count

def part2() -> int:
    claims = data(full=True)
    g = createGrid(0, 1000, 1000)
    clean = {}
    for cid,start,dims in claims: 
        (row,col), (h,w) = start, dims 
        ok = True 
        for dy in range(h):
            r = row+dy 
            for dx in range(w):
                c = col+dx 
                if g[r][c] == 0:
                    g[r][c] = cid # set owner if not yet owned
                else:
                    ok = False 
                    owner = g[r][c]
                    if owner in clean: del clean[owner]
        if ok:
            clean[cid] = True 
    
    claimID = list(clean.keys())[0]
    return claimID

if __name__ == '__main__':
    do(solve, 18, 3)

'''
Part1:
- Initialize 1000x1000 grid to count = 0 
- Process each claim: starting at (row,col) spanning (h,w), increase grid count
- Count grid cells with count > 1 

Part2:
- Similar claims processing to Part 1, but dont keep count 
- Instead keep track of original owner of cell 
- If another claim processes an already owned cell, it is not a clean claim 
- If all cells processed by the claim don't overlap with anything (yet), add it to clean list
- Previously clean claims will be removed if a cell they own is claimed by another 
'''