# Advent of Code 2019 Day 03
# John Roy Daradal 

from aoc import *

T: dict[str,delta] = {'U': U, 'D': D, 'L': L, 'R': R}

def data(full: bool) -> list[list[strInt]]:
    fn = lambda line: [toStrInt(x, 1) for x in line.split(',')]
    return [fn(line) for line in readLines(19, 3, full)]

def solve() -> Solution:
    wires = data(full=True)
    cross = crossingPoints(wires)

    # Part 1
    closest1 = min(manhattan(c) for c in cross)
    
    # Part 2 
    closest2 = min(cross.values())

    return newSolution(closest1, closest2)

def wire(moves: list[strInt]) -> dict[coords,int]:
    visited = {}
    c = (0,0)
    i = 0 
    for k, steps in moves:
        d = T[k]
        for _ in range(steps):
            c = move(c, d)
            i += 1 
            if c not in visited:
                visited[c] = i 
    return visited

def crossingPoints(wires: list[list[strInt]]) -> dict[coords,int]:
    steps = defaultdict(list)
    for moves in wires:
        visited = wire(moves)
        for c,x in visited.items():
            steps[c].append(x)

    cross = {c: sum(s) for c,s in steps.items() if len(s) > 1}
    return cross

if __name__ == '__main__':
    do(solve, 19, 3)

'''
Part1:
- Get the crossing coords of the two wires
- Return the min manhattan distance of all crossing coords

Part2:
- Get the crossing coords of the two wires
- Find the crossing coord with min sum(numSteps)

Wire:
- Start at (0,0), lay out the wire by following the directions (UDLR) and no. of steps 
- Keep track of the step count 
- Each time a new coord is visited, save the current step count
- Return visited coords and their first-encounter step counts

CrossingPoints:
- Lay out the 2 wires on the grid
- For each wire's visited coords: keep track of list which stores numSteps for each wire 
- Crossing points are coords where len(list) > 1 
- Also return the sum of numSteps associated for each coords
'''