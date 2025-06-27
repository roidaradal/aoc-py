# Advent of Code 2017 Day 16
# John Roy Daradal 

from aoc import *

class Dance:
    def __init__(self, line: str):
        self.line = line
        self.kind = line[0]
        self.count: int = 0         # for spin 
        self.indexes: int2 = (0,0)  # for exchange 
        self.pair: str2 = ('','')   # for partner
        match self.kind:
            case 's': 
                self.count = int(line[1:])
            case 'x':
                self.indexes = toInt2(line[1:], '/')
            case 'p':
                self.pair = toStr2(line[1:], '/')
    
    def __repr__(self):
        return self.line

def data(full: bool) -> list[Dance]:
    line = readFirstLine(17, 16, full)
    return [Dance(dance) for dance in splitStr(line, ',')]

def solve() -> Solution:
    dances = data(full=True)
    start, end = 'a', 'p'
    programs = [chr(x) for x in range(ord(start), ord(end)+1)]

    results: list[str] = []
    idx, loopLength = 0, 0
    while True:
        programs = runDances(dances, programs)
        state = ''.join(programs)
        if state in results:
            idx = results.index(state)
            loopLength = len(results) - idx
            break
        results.append(state)

    # Part 1 
    state1 = results[0]

    # Part 2 
    cycles = 1_000_000_000
    cycles = (cycles-1) - idx # -1 for index mode, -idx to remove loop prefix
    loopIdx = cycles % loopLength
    state2 = results[idx + loopIdx]

    return newSolution(state1, state2)

def runDances(dances: list[Dance], programs: list[str]) -> list[str]:
    for dance in dances:
        match dance.kind:
            case 's':
                programs = programs[-dance.count:] + programs[:-dance.count]
            case 'x':
                i, j = dance.indexes
                programs[i], programs[j] = programs[j], programs[i]
            case 'p':
                a, b = dance.pair 
                i, j = programs.index(a), programs.index(b)
                programs[i], programs[j] = programs[j], programs[i]
    return programs

if __name__ == '__main__':
    do(solve, 17, 16)

'''
Solve:
- Initialize the programs with list a-p: [a, b, c, ..., n, o, p]
- For Part 1, do the whole dance once and output the program state after 
- For Part 2, do the dance 1billion times and output the program state after 
- Process each dance move, depending on its kind:
    - If spin, move the last count programs to the front, keeping the order 
    - If exchange, swap the programs at the given indexes 
    - If partner, swap the two given programs (find their indexes)
- Instead of running 1billion times, remember the program states after each dance 
  and find the loop (a state already produced before)
- After we find the state loop, determine the time it was first encountered and the loop length 
- Number of cycles = 1billion - 1 (for index mode) - prefix length
- loopIdx = cycles % loopLength => determines the state index of the 1Bth state
- Similar to 2314 in finding the loop instead of doing 1billion steps
'''