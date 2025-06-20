# Advent of Code 2016 Day 02
# John Roy Daradal 

from aoc import * 

T: dict[str,delta] = {'U': U, 'D': D, 'L': L, 'R': R}

def data(full: bool) -> list[str]:
    return readLines(16, 2, full)

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> str:
    cfg = Config()
    cfg.pad = ['123','456','789']
    cfg.start = (1,1)
    cfg.bounds = (3, 3)
    
    movesList = data(full=True)
    code = solveCode(cfg, movesList)
    return code

def part2() -> str:
    cfg = Config()
    cfg.pad = ['00100','02340','56789','0ABC0','00D00']
    cfg.start = (2,0)
    cfg.bounds = (5, 5)

    movesList = data(full=True)
    code = solveCode(cfg, movesList)
    return code

class Config:
    def __init__(self):
        self.pad: list[str] = []
        self.start: coords = (0,0)
        self.bounds: dims2 = (0,0)

def solveCode(cfg: Config, movesList: list[str]) -> str:
    code = []
    curr = cfg.start
    for moves in movesList:
        for m in moves:
            nxt = move(curr, T[m])
            r, c = nxt
            if insideBounds(nxt, cfg.bounds) and cfg.pad[r][c] != '0':
                curr = nxt 
        row,col = curr 
        code.append(cfg.pad[row][col])
    return ''.join(code)


if __name__ == '__main__':
    do(solve, 16, 2)

'''
Part1:
- Start at (1,1) = "5"
- Process moves UDLR: moving coords by delta
- Ignore if move makes coords go out of bounds
- After each line's moves, store current coords location in pad 
- Combine all code results

Part2:
- Diamond pad has '0' chars in grid to represent outside of pad
- Similar processing to Part 1 
- Start at (2,0) = "5" position in diamond pad 
- boundsCheck: check if insideBounds and coords' mapped character in pad is not '0'
'''