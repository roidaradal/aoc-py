# Advent of Code 2020 Day 12
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[strInt]:
    fn = lambda line: toStrInt(line, 1)
    return [fn(line) for line in readLines(20, 12, full)]

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    commands = data(full=True)
    c, d = (0,0), R 
    for cmd, r in commands:
        if cmd == 'N':
            c = repeatMove(c, U, r)
        elif cmd == 'S':
            c = repeatMove(c, D, r)
        elif cmd == 'E':
            c = repeatMove(c, R, r)
        elif cmd == 'W':
            c = repeatMove(c, L, r)
        elif cmd == 'F':
            c = repeatMove(c, d, r)
        elif cmd == 'L':
            r = r // 90 
            for _ in range(r): d = leftOf[d]
        elif cmd == 'R':
            r = r // 90 
            for _ in range(r): d = rightOf[d]
    return manhattan(c)
    
def part2() -> int:
    commands = data(full=True)
    c, wp = (0,0), (-1, 10)
    for cmd, r in commands:
        if cmd == 'N':
            wp = repeatMove(wp, U, r)
        elif cmd == 'S':
            wp = repeatMove(wp, D, r)
        elif cmd == 'E':
            wp = repeatMove(wp, R, r)
        elif cmd == 'W':
            wp = repeatMove(wp, L, r)
        elif cmd == 'F':
            c = repeatMove(c, wp, r)
        elif cmd == 'L':
            r = r // 90 
            for _ in range(r): wp = turnLeft(wp)
        elif cmd == 'R':
            r = r // 90 
            for _ in range(r): wp = turnRight(wp)
    return manhattan(c)

def waypointDelta(wp: coords) -> delta:
    y,x = wp 
    dy,dx = 0,0 
    if y > 0:
        dy = 1 
    elif y < 0:
        dy = -1 
    if x > 0:
        dx = 1 
    elif x < 0:
        dx = -1 
    return (dy, dx)

def turnLeft(wp: coords) -> coords:
    d = waypointDelta(wp)
    dy, dx = leftOf[d]
    y,x = [abs(i) for i in wp]
    return (dy*x, dx*y) # flip coords 

def turnRight(wp: coords) -> coords:
    d = waypointDelta(wp)
    dy, dx = rightOf[d]
    y,x = [abs(i) for i in wp]
    return (dy*x, dx*y) # flip coords

if __name__ == '__main__':
    do(solve, 20, 12)

'''
Part1:
- Start position at (0,0), direction = R
- Process (command, repeat) pairs
- If command is N/E/W/S: repeatedly move the current position U/R/L/D 
- If command is L/R: divide repeat by 90, repeatedly change the direction to the left / right
- If command is F: repeatedly move the current position with current direction 
- Return the Manhattan distance from origin of resulting position 

Part2:
- Start at position (0,0), waypoint = (-1, 10)
- If command is N/E/W/S: repeatedly move the waypoint U/R/L/D 
- If command is F: repeatedly move the current position using the waypoint as the delta 
- If command is L/R: divide repeat by 90, repeatedly turnLeft / turnRight the waypoint
    - First, compute the waypointDelta: dy and dx is -1 if the y/x value is negative, 1 if positive, else 0
    - TurnLeft/TurnRight the waypointDelta (except if 0,0 = stay put)
    - Get the absolute values of the y and x coordinate of the waypoint 
    - Then flip the magnitude of the coords, but keep the sign of dy, dx
- Return the Manhattan distance from origin of resulting position
'''