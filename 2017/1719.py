# Advent of Code 2017 Day 19
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[str]:
    def fn(line: str) -> str:
        return line.strip('\n')
    return [fn(line) for line in readLines(17, 19, full, strip=False)]

OPP = {U: D, D: U, L: R, R: L}

def solve() -> Solution:
    grid = data(full=True)
    bounds = getBounds(grid)

    # Find the start point in first row
    col = [col for col,char in enumerate(grid[0]) if char == '|'][0]
    curr: coords = (0, col)
    d = D
    
    letters: list[str] = []
    steps = 0
    while True:
        y,x = curr 
        tile = grid[y][x]
        if tile == ' ': break # end of the line

        if tile == '+':
            for d2 in (U,D,L,R):
                nxt = move(curr, d2)
                ny,nx = nxt

                if d2 == OPP[d]: continue # dont go back to previous
                if not insideBounds(nxt, bounds): continue
                if grid[ny][nx] == ' ': continue 

                d = d2 
                break
        elif tile != '|' and tile != '-': # found letter
            # Part 1
            letters.append(tile)
        
        curr = move(curr, d)
        # Part 2
        steps += 1

    message = ''.join(letters)
    return newSolution(message, steps)

if __name__ == '__main__':
    do(solve, 17, 19)

'''
Solve: 
- Find the starting point at the first row (|), initial direction is down 
- At the current position, check the current tile:
- If blank, we stop since we have reached the end of the line 
- If we find a letter, we add it to the letters list 
- If we find a corner +, find the next direction to turn to:
    - Exclude the opposite direction of the current (dont go back to previous = thrash)
    - Skip if this direction leads you out of bounds or has empty tile
    - After finding a | - or letter, we use this as new direction
- We move to the next location with the current direction
- For Part 1, output the letters encountered 
- For Part 2, output the number of steps done before finishing
'''