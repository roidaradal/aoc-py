# Advent of Code 2016 Day 13
# John Roy Daradal 

from aoc import *

def data(full: bool) -> int:
    line = readLines(16, 13, full)[0]
    return int(line)

def solve():
    number = data(full=True)
    steps = bfsTraversal(number, (39,31), 0)
    print(steps)
    count = bfsTraversal(number, None, 50)
    print(count)
    
def bfsTraversal(number: int, goal: coords|None, maxSteps: int) -> int:
    start = (1,1)
    q: list[tuple[coords,int]] = [(start, 0)]
    visited: set[coords] = set()
    gridOpen: dict[coords,bool] = {}
    while len(q) > 0:
        curr, steps = q.pop(0)
        if goal != None and curr == goal:
            return steps
        if curr in visited: continue 
        visited.add(curr)
        nxtSteps = steps + 1
        for nxt in surround4(curr):
            if not isValid(nxt) or nxt in visited: continue 
            if nxt not in gridOpen:
                gridOpen[nxt] = isOpen(nxt, number)
            if not gridOpen[nxt]: continue 
            if maxSteps == 0 or nxtSteps <= maxSteps:
                q.append((nxt, nxtSteps)) 
    return len(visited)

def isOpen(c: coords, number: int) -> bool:
    y,x = c 
    value = (x*x) + (3*x) + (2*x*y) + y + (y*y) + number 
    binary = bin(value)[2:]
    freq = charFreq(binary)
    return freq['1'] % 2 == 0

def isValid(c: coords) -> bool:
    row, col = c 
    return 0 <= row and 0 <= col

if __name__ == '__main__':
    do(solve)

'''
Solve:
- Start at (1,1) with 0 steps; use BFS to traverse the grid 
- If the BFS is goal-based and we have dequeued the goal coords, return the number of steps 
- Keep track of the visited nodes 
- For each neighbor coord (NEWS), check if not out of bounds (must be positive) and not visited 
- Check if the grid is open or walled on the next location by computing the ff:
    - Compute the value given by the formula x^2 + 3x + 2xy + y + y^2 + number, 
      where y,x is the current coords and number is the data input 
    - Get the binary representation of the value
    - Cell is open if number of 1s in the binary is even
- Skip neighbor if not open 
- If BFS is bounded by maxSteps (Part 2), only add to the queue if steps+1 <= maxSteps
- For Part 1, find the minimum number of steps needed to reach (39,31)
- For Part 2, find the number of visited coords in 50 steps or less
'''