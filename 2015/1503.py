# Advent of Code 2015 Day 03
# John Roy Daradal 

from aoc import * 

T: dict[str, delta] = {
    '>' : R,
    '<' : L,
    '^' : U,
    'v' : D,
}

def data(full: bool) -> list[delta]:
    line = readLines(15, 3, full)[0]
    return [T[x] for x in line]

def part1():
    moves = data(full=True)
    visited = walk(moves)
    print(len(visited))

def part2():
    moves = data(full=True)
    m = len(moves)
    v1 = walk(moves[0:m-1:2])  # Santa = Even
    v2 = walk(moves[1:m:2])    # Robo  = Odd
    print(len(v1.union(v2)))

def walk(moves: list[delta], start: coords = (0,0),  visitStart: bool = True) -> set[coords]:
    visited = set()
    if visitStart: visited.add(start)
    curr = start
    for d in moves:
        curr = move(curr, d)
        visited.add(curr) 
    return visited

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Data:
- Translate < left  (0,-1)
- Translate > right (0,1)
- Translate ^ up    (-1,0)
- Translate v down  (1,0)

Part1:
- Start at (0,0)
- Apply all deltas in succession to current coords
- Keep set of visited coords

Part2:
- Similar processing to Part 1
- Separate coords for santa and robo 
- Even moves for santa, odd moves for robo
- Get union of santa and robo's visited
'''