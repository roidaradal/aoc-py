# Advent of Code 2022 Day 23
# John Roy Daradal 

from aoc import *

Grid = dict[coords, bool]

directions: dict[str, delta] = {
    'n': U, 's': D, 'w': L, 'e': R,
    'nw': NW, 'ne': NE, 'sw': SW, 'se': SE,
}

rules: list[tuple[list[str], str]] = [
    (['n', 'ne', 'nw'], 'n'),
    (['s', 'se', 'sw'], 's'),
    (['w', 'nw', 'sw'], 'w'),
    (['e', 'ne', 'se'], 'e'),

]

def data(full: bool) -> Grid:
    grid: Grid = defaultdict(bool)
    lines = readLines(22, 23, full)
    for row, line in enumerate(lines):
        for col, tile in enumerate(line):
            if tile == '#':
                grid[(row,col)] = True
    return grid

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    grid = data(full=True)

    ruleIdx = 0
    for _ in range(10):
        grid, _ = nextGrid(grid, ruleIdx)
        ruleIdx = (ruleIdx + 1) % 4

    (ymin, ymax), (xmin, xmax) = gridBounds(grid)
    count = 0 
    for y in range(ymin, ymax+1):
        for x in range(xmin, xmax+1):
            if grid[(y,x)] == False:
                count += 1

    return count

def part2() -> int:
    grid = data(full=True)

    ruleIdx = 0
    rounds = 0
    while True:
        rounds += 1
        grid, count = nextGrid(grid, ruleIdx)
        ruleIdx = (ruleIdx + 1) % 4
        if count == 0: break 
    
    return rounds

def gridBounds(grid: Grid) -> tuple[int2, int2]:
    ys = [c[0] for c in grid.keys() if grid[c]]
    xs = [c[1] for c in grid.keys() if grid[c]]
    ymin, ymax = min(ys), max(ys)
    xmin, xmax = min(xs), max(xs)
    return (ymin, ymax), (xmin, xmax)

def nextGrid(grid: Grid, ruleIdx: int) -> tuple[Grid, int]:
    elves: dict[coords, dict[str, coords]] = {}
    for curr, isElf in grid.items():
        if not isElf: continue
        elves[curr] = {}
        for k,d in directions.items():
            elves[curr][k] = move(curr, d)

    proposals: dict[coords, list[coords]] = defaultdict(list)
    for elf, neighbors in elves.items():
        # skip if none of the neighbor tiles have elves
        if all(nxt not in grid for nxt in neighbors.values()):
            continue
        # go through rules and select first valid one
        for offset in range(4):
            idx = (ruleIdx + offset) % 4
            keys, moveKey = rules[idx]
            if all(neighbors[k] not in grid for k in keys):
                nxt = neighbors[moveKey]
                proposals[nxt].append(elf)
                break

    grid2: Grid = defaultdict(bool)
    for pos, flag in grid.items():
        grid2[pos] = flag 
    
    # move the proposing elves that are alone in that cell
    count = 0
    for nxt, candidates in proposals.items():
        if len(candidates) > 1: continue # skip if not alone 
        curr = candidates[0]
        del grid2[curr]
        grid2[nxt] = True
        count += 1

    return grid2, count

if __name__ == '__main__':
    do(solve, 22, 23)

'''
Part1:
- Represent the grid as a dictionary of coords => bool (elf/not)
- Start with rule index at 0; after each round, increment the rule index, wrap-around if necessary
- For 10 rounds, compute the next grid:
    - For each elf in the grid, check their 8 neighbor tiles
    - Proposal round: each elf proposes where they will go next 
        - If none of the 8 neighbors have another elf, this elf will not do anything
        - Starting from the current rule index, go through the 4 rules in order, and 
          select the direction of the first valid rule
        - For each rule, it checks that none of the test directions (keys) have elves; 
          if so, the elf will propose to move to the given direction (moveKey)
        - Proposed elf destinations group together the elves that proposed to go there
    - Moving round: an elf who is alone in proposing to move to a destination will move there
        - Skip proposed destinations with more than 1 candidates
        - Update the next grid: current position will be free (False) and next position will have elf (True)
        - Count the number of elves who moved in this round (for Part 2)
- Get the min/max y and x coords with elves
- From the box formed by the bounds above, count the number of tiles without elf

Part2:
- Start with rule index at 0, and update after each round similar to Part 1
- Repeatedly compute the next grid, until we dont find movement from the elves
- Output the first round number where the elves didn't move
'''