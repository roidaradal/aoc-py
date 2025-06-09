# Advent of Code 2018 Day 13
# John Roy Daradal 

from aoc import *

Cart = tuple[delta,int]

class Problem:
    def __init__(self):
        self.next: dict[coords,dict[delta, delta]] = defaultdict(dict)
        self.carts: dict[coords,Cart] = {}

def data(full: bool) -> Problem:
    p = Problem()
    grid = readLines(18, 13, full, False)
    for row, line in enumerate(grid):
        line = line.strip('\n')
        for col, char in enumerate(line):
            if char == ' ': continue 
            pt = (row,col)

            if char in ('|', '^', 'v'): 
                p.next[pt] = {U: U, D: D}
                if char == '^':
                    p.carts[pt] = (U, 0)
                elif char == 'v':
                    p.carts[pt] = (D, 0)
            elif char in ('-', '>', '<'):
                p.next[pt] = {L: L, R: R}
                if char == '<':
                    p.carts[pt] = (L, 0)
                elif char == '>':
                    p.carts[pt] = (R, 0)
            elif char == '/':
                p.next[pt] = {U: R, R: U, L: D, D: L}
            elif char == '\\':
                p.next[pt] = {U: L, L: U, R: D, D: R}
            elif char == '+':
                p.next[pt] = {}
    return p

def solve():
    p = data(full=True)
    pt = findCartPoint(p, True)
    print(pt)
    pt = findCartPoint(p, False)
    print(pt) 

def findCartPoint(p: Problem, firstCrash: bool) -> str:
    cartTurn = {0: L, 1: (0,0), 2: R}
    carts = p.carts 
    while True:
        crashed: set[coords] = set()
        carts2: dict[coords,Cart] = {}
        curr = {c: True for c in carts} 
        for c in sorted(carts.keys()):
            if c in crashed: continue 

            d, t = carts[c]
            del curr[c]
            c = move(c, d)
            if c in curr: # Crash
                if firstCrash:
                    y, x = c 
                    return '%d,%d' % (x,y)
                else:
                    if c in carts2: del carts2[c]
                    crashed.add(c)
                    continue 

            curr[c] = True 
            if len(p.next[c]) == 0:
                d2 = cartTurn[t % 3]
                if d2 == L:
                    d = leftOf[d]
                elif d2 == R:
                    d = rightOf[d]
                t += 1
            else:
                d = p.next[c][d]
            carts2[c] = (d,t)
        carts = carts2
        if len(carts) == 1:
            y, x = list(carts.keys())[0]
            return '%d,%d' % (x,y)


if __name__ == '__main__':
    do(solve)

'''
Data:
- For carts (^v<>), add cart at that coordinate with direction and starting turn index 0
- For vertical characters (|^v), setup the next direction of U-D 
- For horizontal characters (-<>), setup the next direction of L-R 
- If corners (/\\), setup the next direction for U, D, L, R
- If intersection (+), add an empty direction map to trigger turn-index based processing 

FindCardPoint:
- For Part 1, find the point where the cart first crashes
- For Part 2, find the point where the last surviving cart ends up in
- Start with all carts at their starting position and direction
- Loop until first crash is found (Part 1) or only 1 cart remains (Part 2)
- At each round, initialize the set of crashed carts to empty set
- Keep track of current positions of carts (curr)
- Process each cart in row-order manner (based on coordinates)
- Skip carts that were already crashed into 
- Move the cart according to its current direction (remove from previous coord)
- If the resulting coord already has a cart in it: crash happens 
- If only interested in first crash (Part 1), return the coordinates where crash happened 
- Otherwise, remove the crashed carts from current, and add to set of crashed carts
- Figure out the next direction of the cart, based on its current position:
    - If empty direction map, use the turn index % 3
    - If 0, turn left, if 2 turn right, if 1 don't change direction
    - Increment the turn index of the cart for next time 
    - If has direction map, get the next delta of the current delta
'''