# Advent of Code 2016 Day 01
# John Roy Daradal 

from aoc import * 

def data(full: bool) -> list[strInt]:
    line = readFirstLine(16, 1, full)
    return [toStrInt(x, 1) for x in line.split(',')]

def solve() -> Solution:
    moves = data(full=True)

    # Part 1
    hq = findHQ(moves, False)
    dist1 = manhattan(hq)

    # Part 2 
    hq = findHQ(moves, True)
    dist2 = manhattan(hq)

    return newSolution(dist1, dist2)

def findHQ(moves: list[strInt], atVisitedTwice: bool) -> coords:
    curr = (0, 0)
    d: delta|None = None 
    visited = set()
    for turn, steps in moves:
        if d is None: 
            d = L if turn == 'L' else R 
        elif turn == 'L':
            d = leftOf[d]
        elif turn == 'R':
            d = rightOf[d]
        for _ in range(steps):
            curr = move(curr, d)
            if atVisitedTwice and curr in visited:
                return curr 
            visited.add(curr)
    return curr


if __name__ == '__main__':
    do(solve, 16, 1)

'''
Part1:
- Initialize: coords = (0,0), delta = first turn
- Process (turn,steps) sequentially 
- Apply turn left or turn right to current delta
- Repeatedly move coords by numSteps
- Manhattan distance: sum of abs(row) + abs(col) of final coords

Part2:
- Same walk as in Part 1 
- Keep set of visited coords 
- After each move, check if resulting coords is already visited
- Return the first coords that is already visited
'''