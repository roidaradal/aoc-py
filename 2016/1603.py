# Advent of Code 2016 Day 03
# John Roy Daradal 

from aoc import * 

def data(full: bool) -> list[dims3]:
    fn = lambda line: toDims3(line, None)
    return [fn(line) for line in readLines(16, 3, full)]

def solve() -> Solution:
    triples = data(full=True)

    # Part 1
    count1 = countValid(triples, isValid)

    # Part 2 
    triples = readVertical(triples)
    count2 = countValid(triples, isValid)

    return newSolution(count1, count2)

def isValid(triple: dims3) -> bool:
    a,b,c = triple 
    return (a+b > c) and (b+c > a) and (a+c > b)

def readVertical(t: list[dims3]) -> list[dims3]:
    t2 = []
    for r in range(0, len(t), 3):
        for c in range(3):
            t2.append((t[r][c], t[r+1][c], t[r+2][c]))
    return t2

if __name__ == '__main__':
    do(solve, 16, 3)

'''
Part1:
- Loop through each triple 
- Increment count if valid 
- Valid if all sums of two sides > other side

Part2:
- Same processing as Part 1 
- Extract triples vertically 
- Go through rows 3 at a time, collecting the triples at each column
'''