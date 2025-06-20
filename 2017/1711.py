# Advent of Code 2017 Day 11
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[str]:
    line = readFirstLine(17, 11, full)
    return splitStr(line, ',')

N, S, NW, NE, SW, SE = 'n', 's', 'nw', 'ne', 'sw', 'se'

OPP = {
    N : S,
    S : N, 
    NW: SE,
    NE: SW,
    SW: NE, 
    SE: NW,
}

# Result of applying two directions together
RES = {
    N : {SW: NW, SE: NE},
    S : {NW: SW, NE: SE},
    NW: {NE: N, S: SW},
    NE: {NW: N, S: SE},
    SW: {SE: S, N: NW},
    SE: {SW: S, N: NE},
}


def solve() -> Solution:
    steps = data(full=True)
    path: list[str] = []
    maxSteps = 0 
    for step in steps:
        opp = OPP[step]
        opps = [i for i in range(len(path)) if path[i] == opp]
        if len(opps) > 0:
            idx = max(opps) # get last 
            del path[idx]
            continue 
        i = len(path)-1 
        while i >= 0:
            prev = path[i]
            if step in RES[prev]:
                path[i] = RES[prev][step]
                break 
            i -= 1
        else:
            path.append(step)
        maxSteps = max(maxSteps, len(path))
    # Part 1 and 2 
    return newSolution(len(path), maxSteps)

if __name__ == '__main__':
    do(solve, 17, 11)

'''
Solve: 
- OPP maps the opposite directions
- RES maps the result of applying two directions together (used to reduce the path)
- Process each step; start by getting its opposite direction
- If there is an opp direction in the current path, remove the latest one and continue 
- Otherwise, start from the back of the path going to the front 
- Check if applying prev+step is in RES map: we can transform that step
- If no transformation applies, add the step to the path
- For Part 1, output the length of the path after processing all steps 
- For Part 2, output the maximum length of the path encountered during the loop
'''