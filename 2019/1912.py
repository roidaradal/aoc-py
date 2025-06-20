# Advent of Code 2019 Day 12
# John Roy Daradal 

import itertools, math
from aoc import *

class Moon:
    def __init__(self, pos: int3, velocity: int3):
        self.pos = pos 
        self.velocity = velocity
    
    @property 
    def energy(self) -> int:
        pot = sum(abs(x) for x in self.pos)
        kin = sum(abs(x) for x in self.velocity)
        return pot * kin
    
    def move(self):
        x,y,z = self.pos 
        dx,dy,dz = self.velocity 
        self.pos = (x+dx, y+dy, z+dz)

    def updateVelocity(self, diffs: list[int]):
        v1,v2,v3 = self.velocity 
        d1,d2,d3 = diffs 
        self.velocity = (v1+d1, v2+d2, v3+d3)

def data(full: bool) -> list[Moon]:
    def fn(line: str) -> Moon:
        line = line.strip('<>')
        parts = splitStr(line, ",")
        x, y, z = [int(p.split('=')[1]) for p in parts]
        return Moon((x,y,z), (0,0,0))
    return [fn(line) for line in readLines(19, 12, full)]

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    moons = data(full=True)
    for _ in range(1000):
        updateMoons(moons)
    total = sum(m.energy for m in moons)
    return total

def part2() -> int:
    moons = data(full=True)
    ix = moonState(moons, 0)
    iy = moonState(moons, 1)
    iz = moonState(moons, 2)
    found: dict[str,int] = {}

    i = 0
    while len(found) != 3:
        updateMoons(moons)
        i += 1 
        if 'x' not in found and moonState(moons, 0) == ix:
            found['x'] = i 
        if 'y' not in found and moonState(moons, 1) == iy:
            found['y'] = i 
        if 'z' not in found and moonState(moons, 2) == iz:
            found['z'] = i
    
    x, y, z = found['x'], found['y'], found['z']
    return math.lcm(x, y, z)

def updateMoons(moons: list[Moon]):
    for m1, m2 in itertools.combinations(moons, 2):
        d1s: list[int] = []
        d2s: list[int] = []
        for i in range(3):
            d1 = -cmp(m1.pos[i], m2.pos[i])
            d2 = -cmp(m2.pos[i], m1.pos[i])
            d1s.append(d1)
            d2s.append(d2)
        m1.updateVelocity(d1s)
        m2.updateVelocity(d2s)

    for moon in moons:
        moon.move()

def moonState(moons: list[Moon], idx: int) -> tuple[tuple[int,int],...]:
    return tuple((m.pos[idx], m.velocity[idx]) for m in moons)

if __name__ == '__main__':
    do(solve, 19, 12)

'''
Part1:
- Update the moons 1000x 
- Output the total energy of the moons:
    - Potential energy = sum of absolute values of moon's x, y, z  (position)
    - Kinetic energy = sum of absolute values of moon's dx, dy, dz (velocity)
    - Energy = potential * kinetic

Part2:
- Get the initial state of each axis:
    - State of the moons at an axis is represented by 
      the position and velocity values at that axis for each moon
- Loop until we find the loop step for each axis, updating the moons in each round
- Find the loop (same position and velocity as initial) per axis (x,y,z)
- Find the LCM of the steps needed to loop for x, y, z

UpdateMoons:
- Go through each moon pair combination
- For each axis (x, y, z), compare the position value at that axis between the two moons
    - The smaller distance increases velocity by 1 in this axis
    - The bigger distance decreases velocity by 1 in this axis
- Move each moon by applying the velocity at each axis to the current positions

'''