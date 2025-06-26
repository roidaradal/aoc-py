# Advent of Code 2024 Day 13
# John Roy Daradal 

from aoc import *

Config = tuple[delta, delta, coords] # A, B, goal

def data(far: bool, full: bool) -> list[Config]:
    cfgs: list[Config] = []
    a: delta = X
    b: delta = X
    c: coords = (0,0)
    adjust = 10_000_000_000_000
    for line in readLines(24, 13, full):
        if line.startswith('Button A:'):
            dx,dy = extractInt2(line, '+')
            a = (dy,dx)
        elif line.startswith('Button B:'):
            dx,dy = extractInt2(line, '+')
            b = (dy,dx)
        elif line.startswith('Prize:'):
            x,y = extractInt2(line, '=')
            if far: 
                y += adjust
                x += adjust
            c = (y,x)
        elif line == '':
            cfgs.append((a,b,c))
    cfgs.append((a,b,c))
    return cfgs

def extractInt2(line: str, sep: str) -> int2:
    line = splitStr(line, ':')[1]
    for remove in ['X'+sep, 'Y'+sep]: line = line.replace(remove, '')
    return toInt2(line, ',')

def solve() -> Solution:
    # Part 1 
    cfgs = data(far=False, full=True)
    fn1 = lambda cfg: solveSysLinEq(cfg, 100)
    total1 = getTotal(cfgs, fn1)

    # Part 2
    cfgs = data(far=True, full=True)
    fn2 = lambda cfg: solveSysLinEq(cfg, 0)
    total2 = getTotal(cfgs, fn2)

    return newSolution(total1, total2)

def solveSysLinEq(cfg: Config, clip: int) -> int:
    da, db, goal = cfg
    ay, ax = da 
    by, bx = db 
    gy, gx = goal

    numerator = -ax 
    denominator = ay 

    # Solve for B
    left = (bx * denominator) + (by * numerator)
    right = (gx * denominator) + (gy * numerator)
    b = right // left 
    
    # Solve for A using Equation 1 
    a = (gx - (bx*b)) // ax 

    # Check restrictions on A,B value
    if clip > 0 and (a > clip or b > clip): 
        return 0
    if a < 0 or b < 0:
        return 0
    
    # Validate on Equation 1
    result = (ax * a) + (bx * b) - gx 
    if result != 0:
        return 0

    # Validate on Equation 2 
    result = (ay * a) + (by * b) - gy 
    if result != 0:
        return 0
    
    costA, costB = 3, 1
    return (a*costA) + (b*costB)

if __name__ == '__main__':
    do(solve, 24, 13)

'''
Solve: 
- For Part 1, get the total cost of winnable games, where A and B are clipped at 100
- For Part 2, add 10 trillion to the goal coordinates, and solve the total cost of winnable games 
- Use system of linear equations (2 equations, 2 unknowns) to solve the problem
    - 2 variables: A and B = no. of times to press A and B that will reach the goal
    - Solve for the values of A and B, then validate on equation 1 and equation 2 if valid
    - Cost of the game is 3*A + B
'''