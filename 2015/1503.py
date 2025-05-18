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
    _, visited = walk(moves)
    print(len(visited))

def part2():
    moves = data(full=True)
    m = len(moves)
    _, visited1 = walk(moves[0:m-1:2])  # Santa = Even
    _, visited2 = walk(moves[1:m:2])    # Robo  = Odd
    v1 = set(visited1.keys())
    v2 = set(visited2.keys())
    print(len(v1.union(v2)))

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