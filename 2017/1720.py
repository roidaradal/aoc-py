# Advent of Code 2017 Day 20
# John Roy Daradal 

from aoc import *

class Particle:
    def __init__(self, line: str):
        for remove in ('p=<', 'v=<', 'a=<'):
            line = line.replace(remove, '')
        line = line.replace('>, ', ',').strip('>')
        px,py,pz,vx,vy,vz,ax,ay,az = toIntList(line, ',')
        self.curr: int3     = (px, py, pz)
        self.speed: int3    = (vx, vy, vz)
        self.accel: int3    = (ax, ay, az)
        self.lastDistance   = manhattan3(self.curr)
        self.lastIncrease   = 0 
        self.lastDecrease   = 0
    
    def move(self, t: int):
        px, py, pz = self.curr
        vx, vy, vz = self.speed 
        ax, ay, az = self.accel 
        vx += ax; vy += ay; vz += az 
        px += vx; py += vy; pz += vz
        self.speed = (vx, vy, vz)
        self.curr  = (px, py, pz)
        distance = manhattan3(self.curr)
        if distance > self.lastDistance:
            self.lastIncrease = t 
        elif distance < self.lastDistance:
            self.lastDecrease = t
        self.lastDistance = distance

    @property 
    def isStable(self) -> bool:
        diff = abs(self.lastIncrease - self.lastDecrease)
        return diff >= 500

def data(full: bool) -> list[Particle]:
    return [Particle(line) for line in readLines(17, 20, full)]

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    particles = data(full=True)
    t = 1 
    while True:
        for p in particles:
            p.move(t)
        if all(p.isStable for p in particles): break
        t += 1
    options = [(p.lastDistance, i) for i,p in enumerate(particles)]
    _, pid = min(options)
    return pid

def part2() -> int:
    particles = data(full=True)
    active: dict[int, Particle] = {}
    for i,p in enumerate(particles):
        active[i] = p

    t = 1
    while True:
        occupied: dict[int3, list[int]] = defaultdict(list)
        for i,p in active.items():
            p.move(t)
            occupied[p.curr].append(i)
        
        for clash in occupied.values():
            if len(clash) == 1: continue 
            for i in clash:
                del active[i]

        if all(p.isStable for p in active.values()): break
        t += 1
             
    return len(active)

if __name__ == '__main__':
    do(solve, 17, 20)

'''
Part1:
- Move each particle simultaneously:
    - Adjust the velocity x, y, z by adding the acceleration x, y, z 
    - Adjust the position x, y, z by adding the velocity x, y, z 
    - Compute the new position's Manhattan distance 
    - If increased from lastDistance, update lastIncrease to now 
    - If decreased from lastDistance, update lastDecrease to now
    - Remember this new distance as lastDistance for next round
- Stop if all particles are already stable
    - A particle is stable if it has been steadily increasing/decreasing for a long time
    - Get the abs difference of lastIncrease and lastDecrease 
    - If the diff passes the stable factor, the particle is already stable
- Experimented with stable factor values: 10, 100, 200, 500, 1000 and checked when 
  even increasing the stable factor yields the same result; settled with 500
- After finding stable state, find the particle closest to the origin 

Part2:
- Similar to Part 1, but we keep a dictionary of pid => active Particle 
- Use a dictionary for easy deletion when they collide with others
- After moving the particles, group together their current positions to detect collisions 
- Remove groups of particles that collided from the active particles 
- If all active particles are stable, we stop and return the number of active particles left
'''