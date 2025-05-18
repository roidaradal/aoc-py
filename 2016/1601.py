# Advent of Code 2016 Day 01
# John Roy Daradal 

from aoc import * 

def data(full: bool) -> list[strInt]:
    line = readLines(16, 1, full)[0]
    return [toStrInt(x, 1) for x in line.split(',')]

def part1():
    moves = data(full=True)
    hq = findHQ(moves, False)
    print(manhattan(hq))

def part2():
    moves = data(full=True)
    hq = findHQ(moves, True)
    print(manhattan(hq))

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
    do(part1)
    do(part2)

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