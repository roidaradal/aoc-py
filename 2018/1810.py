# Advent of Code 2018 Day 10
# John Roy Daradal 

from aoc import *

Particle = tuple[coords, delta] 

def data(full: bool) -> list[Particle]:
    def fn(line: str) -> Particle:
        head, tail = line.split('>', 1)
        head = head.split('<')[1].strip()
        tail = tail.split('<')[1].strip('>')
        x,y = toInt2(head, ',')
        dx,dy = toInt2(tail, ',')
        return (y,x), (dy,dx)
    return [fn(line) for line in readLines(18, 10, full)]

def solve():
    particles = data(full=True)
    areas, states = [], []
    for i in range(15_000):
        particles2 = []
        for c,d in particles:
            c2 = move(c, d)
            particles2.append((c2, d))
        particles = particles2 
        states.append(particles2)
        area = computeArea(particles2)
        areas.append((area, i))
    
    _, idx = min(areas)
    display(states[idx])
    print(idx+1)

def computeArea(particles: list[Particle]) -> int:
    (y1,x1), (y2,x2) = computeBounds(particles)
    h, w = y2-y1, x2-x1 
    return h*w

def display(particles: list[Particle]):
    (y1,x1), (y2,x2) = computeBounds(particles)
    g = {}
    for y in range(y1,y2+1):
        for x in range(x1,x2+1):
            g[(y,x)] = '.'
    for p in particles:
        g[p[0]] = '#'
    
    for y in range(y1,y2+1):
        line = [g[(y,x)] for x in range(x1,x2+1)]
        print(''.join(line))

def computeBounds(particles: list[Particle]) -> tuple[coords, coords]:
    ys = [p[0][0] for p in particles]
    xs = [p[0][1] for p in particles]
    x1,y1 = min(xs), min(ys)
    x2,y2 = max(xs), max(ys)
    return (y1,x1), (y2,x2)

if __name__ == '__main__':
    do(solve)

'''
Solve:
- Run the simulation for 15,000 rounds (could be lower after finding the min idx)
- In each round, move the particles according to their delta
- At each round, compute the area covered by the particles
- Idea: the message must appear when the area is at minimum (compact to form the message, not dispersed)
- Save each round's state, and find the round with minimum area after the simulation
- Print that round's grid
- For Part 2, output the number of seconds needed to display the message
'''