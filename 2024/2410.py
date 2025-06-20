# Advent of Code 2024 Day 10
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[list[int]]:
    return [toIntLine(line) for line in readLines(24, 10, full)]

def solve() -> Solution:
    grid = data(full=True)
    start: list[coords] = []
    for row, line in enumerate(grid):
        for col, x in enumerate(line):
            if x == 0: start.append((row,col)) 

    score: list[int] = []
    rating: list[int] = []
    for c in start:
        reached = count9(c, grid)
        # Part 1
        score.append(len(reached))
        # Part 2
        rating.append(sum(reached.values()))
    
    return newSolution(sum(score), sum(rating))

def count9(start: coords, grid: list[list[int]]) -> dict[coords,int]:
    bounds = getBounds(grid)
    goals: dict[coords,int] = defaultdict(int)
    q = [start]
    while len(q) > 0:
        c = q.pop(0)
        row,col = c 
        value = grid[row][col]
        if value == 9:
            goals[c] += 1 
        else:
            for nxt in surround4(c):
                if not insideBounds(nxt, bounds): continue 
                row, col = nxt 
                if grid[row][col] == value + 1:
                    q.append((row,col))
    return goals


if __name__ == '__main__':
    do(solve, 24, 10)

'''
Solve:
- Find the starting points by going through the grid and finding 0s 
- For each starting point, find the reachable 9s by doing BFS:
    - Keep track of how many times a goal cell (9) is reached 
    - From current cell, check the 4 surrounding cells (if insideBounds)
    - Add to queue if the value is 1 above the current cell
- For Part 1, output the total number of coords reached 
- For Part 2, output the total number of distinct paths to reach a 9
'''