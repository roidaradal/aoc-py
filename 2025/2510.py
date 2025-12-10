# Advent of Code 2025 Day 10
# John Roy Daradal 

from scipy.optimize import linprog
from numpy import transpose
from aoc import *

LightState = tuple[bool,...]

class Config:
    def __init__(self):
        self.goal: LightState = tuple()
        self.buttons: list[list[int]] = []
        self.joltage: list[int] = []

def data(full: bool) -> list[Config]:
    def fn(line: str) -> Config:
        cfg = Config()
        parts = line.split()
        cfg.goal = tuple([char == '#' for char in parts[0].strip('[]')])
        cfg.joltage = [int(x) for x in parts[-1].strip('{}').split(',')]
        cfg.buttons = [toIntList(p.strip('()'),',') for p in parts[1:-1]]
        return cfg
    return [fn(line) for line in readLines(25, 10, full)]

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    configs = data(full=True)
    total = sum(countMinStepsToGoal(cfg) for cfg in configs)
    return total

def countMinStepsToGoal(cfg: Config) -> int:
    start: LightState = tuple([False] * len(cfg.goal))
    q: list[tuple[LightState,int]] = [(start, 0)]
    visited: set[LightState] = set()
    while len(q) > 0:
        curr, steps = q.pop(0)
        if curr == cfg.goal:
            return steps 
        if curr in visited: continue 
        visited.add(curr)
        for button in cfg.buttons:
            nxt = applyButton(curr, button)
            if nxt in visited: continue 
            q.append((nxt, steps+1))
    return 0

def applyButton(curr: LightState, button: list[int]) -> LightState:
    nxt = [flag for flag in curr]
    for idx in button:
        nxt[idx] = not nxt[idx]
    return tuple(nxt)

def part2() -> int:
    configs = data(full=True)
    total = 0
    for cfg in configs:
        numButtons = len(cfg.buttons)
        numJolt = len(cfg.joltage)
        c = [1] * numButtons
        b_eq = cfg.joltage 
        A_eq = [toVector(button, numJolt) for button in cfg.buttons]
        A_eq = transpose(A_eq)
        res = linprog(c, A_eq=A_eq, b_eq=b_eq, integrality=c)
        count = math.ceil(sum(res.x))
        total += count
    return total

def toVector(button: list[int], numSlots: int) -> list[int]:
    vector = [0] * numSlots
    for idx in button: 
        vector[idx] = 1 
    return vector

if __name__ == '__main__':
    do(solve, 25, 10)

'''
Part1:
- Use BFS to look for the shortest path from start state (all off) to goal light state
- For the neighbor states, apply each of the buttons to the current state to produce the next state 
- Output the total minimum steps to reach the goal state for each config

Part2:
- Use SciPy to solve the linear equation
- Coefficient (c) of each button is 1
- Reuse the list of 1s from c to declare integrality (all values must be integers)
- The right side of equality equations (b) are the joltage values 
- The coefficients of left side of inequality are built by converting the button to vector:
    - Initialize with list of zeros, then the indices of the buttons are turned to 1
    - Example: (0,2) for 4 jolt values becomes [1,0,1,0]
- Then, we transpose this matrix to have the correct orientation
- Use linprog from scipy to solve for the linear equation solution
- Use math.ceil because of rounding errors
- The solution values represent how much each button should be pressed
- The minimum steps to reach the joltage counts are the sum of the solution values 
- Output the total minimum steps to reach the jolt counts for each config
'''