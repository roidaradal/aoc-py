# Advent of Code 2025 Day 07
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[str]:
    return readLines(25, 7, full)

def solve() -> Solution:
    grid = data(full=True)
    # Find S in first line 
    start = [col for col,char in enumerate(grid[0]) if char == 'S'][0]
    curr: dict[int,int] = defaultdict(int)
    curr[start] = 1
    numSplit = 0
    for row in range(1, len(grid)):
        nxt: dict[int,int] = defaultdict(int)
        for col, count in curr.items():
            if grid[row][col] == '^':
                numSplit += 1
                nxt[col-1] += count 
                nxt[col+1] += count 
            else:
                nxt[col] += count
        curr = nxt

    numPath = sum(curr.values())
    return newSolution(numSplit, numPath)

if __name__ == '__main__':
    do(solve, 25, 7)

'''
Solve:
- Find the S column from the first line 
- Keep track of the columns containing particles and the number of paths it took to get there from previous rounds
- Initially, this map is start => 1
- Go down through the rows, and for each row build the map for the next round
- For each current column position and their counts:
    - If splitter (^), we add col-1 and col+1 to the next map, with the count, and increment the split count
    - Otherwise, keep the same column for next map, with the count
- For Part 1, output the number of splits
- For Part 2, output the sum of paths from the final mapping of columns => numPaths
'''