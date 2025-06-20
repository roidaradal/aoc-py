# Advent of Code 2015 Day 03
# John Roy Daradal 

from aoc import * 

def data(full: bool) -> list[delta]:
    T: dict[str, delta] = {
        '>' : R,
        '<' : L,
        '^' : U,
        'v' : D,
    }
    line = readFirstLine(15, 3, full)
    return [T[x] for x in line]

def solve() -> Solution:
    moves = data(full=True)

    # Part 1
    visited = walk(moves)
    count1 = len(visited)

    # Part 2
    m = len(moves)
    v1 = walk(moves[0:m-1:2])  # Santa = Even
    v2 = walk(moves[1:m:2])    # Robo  = Odd
    count2 = len(v1.union(v2))

    return newSolution(count1, count2)

def walk(moves: list[delta]) -> set[coords]:
    start = (0,0)
    visited: set[coords]= set()
    visited.add(start)
    curr = start
    for d in moves:
        curr = move(curr, d)
        visited.add(curr) 
    return visited

if __name__ == '__main__':
    do(solve, 15, 3)

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