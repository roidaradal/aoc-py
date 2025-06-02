# Advent of Code 2015 Day 14
# John Roy Daradal 

from aoc import *

class Reindeer:
    def __init__(self, name: str, flySpeed: int, flyTime: int, restTime: int):
        self.name = name 
        self.flySpeed = flySpeed 
        self.flyTime = flyTime 
        self.restTime = restTime 

        self.flyLeft = flyTime 
        self.restLeft = restTime 
        self.isFlying = True
        self.total = 0

def data(full: bool) -> list[Reindeer]:
    def fn(line: str) -> Reindeer:
        p = line.split()
        return Reindeer(p[0], int(p[3]), int(p[6]), int(p[-2]))
    return [fn(line) for line in readLines(15, 14, full)]

def solve():
    reindeers = data(full=True)
    score = {r.name : 0 for r in reindeers}
    for _ in range(2503):
        for reindeer in reindeers:
            tick(reindeer)
        best = max(r.total for r in reindeers)
        for r in reindeers:
            if r.total == best:
                score[r.name] += 1
    
    # Part 1
    maxTotal = max(r.total for r in reindeers)
    print(maxTotal)

    # Part 2 
    maxScore = max(score.values())
    print(maxScore)

def tick(r: Reindeer):
    if r.isFlying:
        r.total += r.flySpeed
        r.flyLeft -= 1
        if r.flyLeft == 0:
            r.isFlying = False 
            r.flyLeft =  r.flyTime
    else:
        r.restLeft -= 1 
        if r.restLeft == 0:
            r.isFlying = True 
            r.restLeft = r.restTime

if __name__ == '__main__':
    do(solve)

'''
Part1:
- For 2503 iterations, run tick on each reindeer
- Output the maximum total out of all reindeers

Part2:
- For 2503 iterations, run tick on each reindeer
- After each round, find the best current total 
- Increment the score of the reindeers with current best total 
- Output the maximum score out of all reindeers


Tick:
- At each second, process each reindeer
- If reindeer.isFlying, add its flySpeed to its total and decrement flyLeft 
- Once flyLeft becomes 0, stop flying and reset the flyLeft back (for next fly)
- If not reindeer.isFlying, decrement restLeft 
- Once restLeft becomes 0, stop resting and fly again, reset restLeft back (for next rest)
'''