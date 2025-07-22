# Advent of Code 2022 Day 19
# John Roy Daradal 

import math
from aoc import *

ORE, CLAY, OBS, GEO = 0, 1, 2, 3

Vector = list[int]
Blueprint = list[Vector]
State = tuple[int, Vector, Vector] # robots, supply

def data(full: bool) -> list[Blueprint]:
    blueprints: list[Blueprint] = []
    for line in readLines(22, 19, full):
        tail = splitStr(line, ':')[1]
        lines = splitStr(tail, '.')
        line1, line2, line3, line4 = [x.split() for x in lines[0:4]]
        ore1 = int(line1[-2])
        clay1 = int(line2[-2])
        obs1, obs2 = int(line3[-5]), int(line3[-2])
        geo1, geo2 = int(line4[-5]), int(line4[-2])
        blueprints.append([
            [ore1, 0, 0, 0], 
            [clay1, 0, 0, 0], 
            [obs1, obs2, 0, 0],
            [geo1, 0, geo2, 0],
        ])
    return blueprints

def solve() -> Solution:
    blueprints = data(full=True)

    # Part 1
    timeLimit = 24
    total = 0
    for i, bp in enumerate(blueprints):
        robotLimits = getRobotLimits(bp, timeLimit)
        maxGeode = getMaxGeode(bp, robotLimits, timeLimit)
        total += (i+1) * maxGeode

    # Part 2
    timeLimit = 32 
    product = 1
    for bp in blueprints[:3]:
        robotLimits = getRobotLimits(bp, timeLimit)
        maxGeode = getMaxGeode(bp, robotLimits, timeLimit)
        product *= maxGeode

    return newSolution(total, product)

def increaseSupply(supply: Vector, robots: Vector, rounds: int = 1) -> Vector:
    return [s+(r * rounds) for s,r in zip(supply, robots)]

def consumeSupply(supply: Vector, req: Vector) -> Vector:
    return [s-r for s,r in zip(supply, req)]

def isReqSatisfied(supply: Vector, req: Vector) -> bool:
    return all(s >= r for s,r in zip(supply, req))

def addRobot(robots: Vector, robot: int) -> Vector:
    return [x+1 if i == robot else x for i,x in enumerate(robots)]

def getRobotLimits(bp: Blueprint, timeLimit: int) -> Vector:
    limits = [max(req[robot] for req in bp) for robot in range(4)]
    limits = [limit if limit > 0 else timeLimit for limit in limits]
    return limits

def getMaxGeode(bp: Blueprint, robotLimits: Vector, timeLimit: int) -> int:
    state: State = (0, [1,0,0,0], [0,0,0,0])
    stack: list[State] = [state]
    maxGeode = 0 
    while len(stack) > 0:
        state = stack.pop()
        minute, _, supply = state 
        if minute == timeLimit:
            maxGeode = max(maxGeode, supply[GEO])
        elif ceilingScore(state, timeLimit) <= maxGeode:
            continue 
        else:
            for nxtState in nextStates(state, bp, robotLimits, timeLimit):
                stack.append(nxtState)
    return maxGeode

def ceilingScore(state: State, timeLimit) -> int:
    minute, robots, supply = state 
    timeLeft = timeLimit - minute
    currentGeo = supply[GEO]            # current Geode count
    futureGeo = timeLeft * robots[GEO]  # future Geodes the geode robots will mine
    relaxGeo = sum(range(timeLeft))     # if we produced 1 Geo robot per minute til the end
    # Unrealistic, but this sets the upper-bounds on the obtainable score from this state
    return currentGeo + futureGeo + relaxGeo

def nextStates(state: State, bp: Blueprint, robotLimits: Vector, timeLimit: int) -> list[State]:
    minute, robots, supply = state
    timeLeft = timeLimit - minute
    branches: list[State] = []

    # Do nothing til the end 
    nxtSupply = increaseSupply(supply, robots, timeLeft)
    branches.append((timeLimit, robots, nxtSupply))

    for robot, req in enumerate(bp):
        # Dont build a robot if robotCount is already at limit
        if robots[robot] == robotLimits[robot]: continue 

        nxtMinute = minute 
        nxtSupply = supply

        steps = stepsToGather(state, req, timeLimit)
        if steps > 0: 
            # Gather requirements
            for _ in range(steps):
                nxtSupply = increaseSupply(nxtSupply, robots)
                nxtMinute += 1
        
        if isReqSatisfied(nxtSupply, req):
            # Build the robot
            nxtSupply = increaseSupply(nxtSupply, robots)
            nxtSupply = consumeSupply(nxtSupply, req)
            nxtRobots = addRobot(robots, robot)
            nxtMinute += 1
            branches.append((nxtMinute, nxtRobots, nxtSupply))

    return branches

def stepsToGather(state: State, req: Vector, timeLimit: int) -> int:
    minute, robots, supply = state 
    timeLeft = timeLimit - minute
    needSteps = []

    for robot, required in enumerate(req):
        # Skip if no need to gather this ingredient
        needToGather = required - supply[robot]
        if needToGather <= 0: continue

        # Stop if missing robot for a needed ingredient
        numRobots = robots[robot]
        if numRobots == 0:  return 0
        
        needSteps.append(math.ceil(needToGather / numRobots))

    if len(needSteps) == 0: return 0
    
    maxSteps = max(needSteps)
    return maxSteps if maxSteps <= timeLeft else 0
        
if __name__ == '__main__':
    do(solve, 22, 19)

'''
Solve:
- Process each available blueprint (in Part 2, you only process 3)
- Get the robot count limits by going through the blueprint recipes and getting the 
  maximum required count for each robot type; if limit is 0, set it to the timeLimit
- We set robot count limits, because if the maximum needed ore by any recipe is 4, we don't 
  need to build more than 4 ore robots as we can only consume max of 4 ores per round (to avoid excess)
- Get the max geode for the blueprint, given the robot count limits, and the timeLimit
- For Part 1, timeLimit = 24, and get the total bpID * bpMaxGeode
- For Part 2, timeLimit = 32, process only the first 3 blueprints, and get the product of their maxGeodes

GetMaxGeode:
- Use Vectors: list of ints to represent the robot counts, supply counts, requirements, robot limits
- Vectors always have 4 items, arranged in the order of ORE, CLAY, OBS, GEO
- Use DFS to explore the possible states, but with pruning to avoid unnecessary explorations
- Choose DFS so we can reach timeLimit faster, set a maxGeode ASAP, which helps the pruning
- Start with the state at minute=0, with 1 ore robot, and 0 supplies
- When the popped state is already at the timeLimit, update the maxGeode if necessary, with the supply[GEO]
- Check if the current state's ceiling score cannot be better than the current maxGeode: if it doesn't 
  improve the score, we skip it (pruning)
    - To compute the ceiling score of a state, we sum up the ff:
    - 1) Current geode count = supply[GEO]
    - 2) Future geodes that can be build = timeLeft * robots[GEO] 
    - 3) Assuming we can produce 1 geode robot for each of the time left: sum(range(timeLeft))
    - #3 is a relaxation of the problem: unrealistic, but it sets the upper-bounds on the obtainable score for this state
    - Example:  if we have 1 minute  left, we can build 1, but harvest 0
                if we have 2 minutes left, we can build 2, and harvest 1
                if we have 3 minutes left, we can build 3, and harvest 2
- Otherwise, we explore the next states by trying to build other robots:
    - Option 1: don't build anything, just gather until the end: we just increase the supplies
      by the number of robots, repeated by the timeLeft, and we fast forward to the end (timeLimit)
    - Option 2: try to build other robots, so check their requirements from the blueprint
    - Check first if the robot count is already at limit; if it is, don't build anymore
    - Check how many steps you need to gather the requirements to build the robot:
        - For each requirement, the amount we need to gather is the required - current supply of that item 
        - If needToGather is <= 0, we skip it: either we dont need it to build the robot, or we have enough supplies for it
        - If we need to gather an item, and there are no robots available for that type, we immediately stop:
          impossible to build this robot, with a missing ingredient robot
        - Otherwise, the needed steps is ceiling of needToGather / numRobots:
            - Example: needToGather = 5, numRobots = 2, needSteps = 3
        - If needSteps is empty, we return 0 (don't need any step to build this requirement)
        - Otherwise, we take the max of needSteps 
        - Check that maxSteps <= timeLeft (otherwise, we'll overshoot the timelimit)
    - For the number of gather steps, repeatedly increase the supply by the current robots, and increment the minute
    - After gathering (or not gathering, because you already have the requirements without even gathering), 
      we check if the current supplies satisfy the requirement: all(supply >= req)
    - If all requirements are satisfied, we build the robot in the next minute:
        - Increase the supply first by the current robots 
        - Consume the supply needed by the requirement to build the robot
        - Update the robot counts, we add 1 more for this robot type
        - Add this to the next state branches
'''