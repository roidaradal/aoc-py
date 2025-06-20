# Advent of Code 2016 Day 11
# John Roy Daradal 

import heapq, math, itertools 
from dataclasses import dataclass
from aoc import *

lastFloor = 3 
class Problem:
    def __init__(self):
        self.items: list[list[int]] = []
        self.goal: tuple[int,int,int,int] = (0,0,0,0)

def data(add: dict[int,list[strInt]], full: bool) -> Problem:
    floors: list[list[strInt]] = []
    elements: set[str] = set()
    numItems: int = 0
    for currFloor, line in enumerate(readLines(16, 11, full)):
        line = line.replace(',', '').strip('.')
        p = line.split()
        gen = [i-1 for i in range(len(p)) if p[i] == 'generator']
        chp = [i-1 for i in range(len(p)) if p[i] == 'microchip']
        floor = []
        for i in gen: floor.append((p[i][0].upper(), 1))
        for i in chp: floor.append((p[i][0].upper(), -1))
        if currFloor in add:
            for item in add[currFloor]: floor.append(item)
        floors.append(floor)
        numItems += len(floor)
        elements = elements.union(set(x[0] for x in floor))
    T = {elem: i+1 for i,elem in enumerate(sorted(elements))}

    problem = Problem()
    problem.items = [sorted(T[elem] * sign for elem,sign in floor) for floor in floors]
    problem.goal = (0,0,0,numItems)
    return problem

def solve() -> Solution:
    additional: list[dict[int,list[strInt]]] = [
        {},                                         # Part 1
        {0: [('E',1),('E',-1),('D',1),('D',-1)]},   # Part 2
    ]
    numSteps = []
    for add in additional:
        problem = data(add, full=True)
        State.problem = problem
        curr = State(0)
        curr.items = problem.items 
        curr.computeKey()
        score = curr.score()

        # StateScore, HeuristicScore, State
        pq: list[tuple[int,int,State]] = [(score, score-curr.steps, curr)]
        visited: set[str] = set()
        i, factor = 0, 100_000
        while len(pq) > 0:
            i += 1
            score, hscore, curr = heapq.heappop(pq)
            if i % factor == 0: print(i//factor, score, hscore)

            if curr.isDone():
                numSteps.append(curr.steps)
                break

            if curr.key in visited: continue 
            visited.add(curr.key)
            for nxt in nextStates(curr):
                if nxt.key in visited: continue 
                score = nxt.score()
                heapq.heappush(pq, (score, score-nxt.steps, nxt))
        
    return newSolution(numSteps[0], numSteps[1]) 

# For ordering state in the heapq
@dataclass(order=True)
class State:
    problem = Problem()

    def __init__(self, elevator: int):
        self.elevator: int = elevator 
        self.items: list[list[int]] = []
        self.steps: int = 0
        self.key: str = '<State>'
        self.parent: State|None = None 

    def __repr__(self) -> str:
        return self.key

    def computeKey(self):
        floors: list[str] = []
        for items in self.items:
            floor = [str(x) for x in sorted(items)]
            floors.append(','.join(floor))
        self.key = '%d:%s' % (self.elevator, '|'.join(floors))

    def isDone(self) -> bool:
        current = tuple(len(x) for x in self.items)
        return current == self.problem.goal
    
    def isValid(self) -> bool:
        for items in self.items:
            if len(items) == 0: continue 
            gen = [x for x in items if x > 0]
            chp = [x for x in items if x < 0]
            if len(gen) == 0 or len(chp) == 0: continue 
            for c in chp:
                if -c not in gen: return False 
        return True

    def score(self) -> int:
        return heuristicScore(self) + self.steps
    
def nextStates(curr: State) -> list[State]:
    # Figure out next floors 
    level = curr.elevator 
    nxtFloors: list[int] = []
    if level < lastFloor:
        nxtFloors.append(level+1)
    # Check if there are items below = go down
    goDown = level > 0 and any(len(curr.items[f]) > 0 for f in range(level)) 
    if goDown:
        nxtFloors.append(level-1)

    states: list[State] = []
    for nxtFloor in nxtFloors:
        items = curr.items[level]
        # Take one 
        for item in items:
            nxt = nextState(curr, nxtFloor)
            nxt.items[level].remove(item)
            nxt.items[nxtFloor].append(item)
            nxt.computeKey()
            if curr.parent != None and nxt.key == curr.parent.key:
                continue # anti-thrashing 
            if nxt.isValid():
                states.append(nxt)

        if nxtFloor < level: continue # dont take two items down 

        # Take two 
        for itemPair in itertools.combinations(items, 2):
            nxt = nextState(curr, nxtFloor)
            for item in itemPair:
                nxt.items[level].remove(item)
                nxt.items[nxtFloor].append(item)
            nxt.computeKey()
            if curr.parent != None and nxt.key == curr.parent.key:
                continue # anti-thrashing
            if nxt.isValid():
                states.append(nxt)
                
    return states
    
def nextState(state: State, elevator: int) -> State:
    nxt = State(elevator)
    nxt.items = [x[:] for x in state.items]
    nxt.steps = state.steps + 1 
    nxt.parent = state 
    return nxt

def heuristicScore(state: State) -> int:
    # Sum up 2*height of carrying two items at a time
    score = 0 
    for floor in range(lastFloor): # dont include last floor 
        count = len(state.items[floor])
        trips = math.ceil(count / 2) # take two at a time
        height = lastFloor - floor 
        score += trips * height * 2  # 2 trips: to last floor and back
    return score

if __name__ == '__main__':
    do(solve, 16, 11)

'''
Data: 
- Collect generators (1) and microchips (-1) using their first letters; use the sign to distinguish gen vs chip
- For Part 2, add the additional generators and chips to level 0 
- Sort the elements and assign a mapping of element to number for easier representation:
  x for the generators and -x for the microchips
- Keep track of the items in each floor 
- Goal is to have all items in the last floor (0,0,0,numItems)

Solve:
- Start with the initial state in the priority queue 
- Use A* search: actual no. of steps + heuristic score becomes the weight for choosing next state
- Keep track of visited states to avoid loops
- Remove the min-score state from the heap PQ 
- If state is done (all items in the last floor), stop the loop and output the state's number of steps 
- If state is already visited, skip 
- For each next state of the current state, skipping the already visited, add these states to the heap PQ

State:
- computeKey(): current elevator level and the representation of each floors
- isValid(): check if state is valid according to chip-generator rules:
    - Check all floors for possible problems; skip if floor is empty
    - Easy to separate gens (positive) and chips (negative)
    - If gens or chips are empty, skip (no problem if all homogeneous)
    - Check each chip, if its corresponding gen (-chip) is not on that floor: invalid 
- nextState(): copy the current state's items, increment the current state's steps, and set current as the parent

NextStates:
- Figure out the next floors: if not yet on lastFloor, add the floor above (+1)
- If there are items below current floor, allowed to go down (-1)
- Try to take one item at a time to produce the next state
- In the next state: remove the item from the current level and add it to the next floor
- Anti-thrashing measure: ensure that this state is not the current's parent:
  Example: state0 = item at 0, state1 = bring item to 1, state2 = bring item down to 0
- Don't take two items down (only need 1) - it's counter-productive
- Try to take two items to produce next state (get all pair combinations)
- In the next state: remove the 2 items from current level, add them to next floor 
- Return valid next states

Heuristic Score:
- Idea: Sum up 2*height of carrying two items at a time
- Excluding the last floor (since this is the goal destination), process each floor:
    - Count the number of items currently on the floor 
    - No. of trips would be ceil(count/2): take two at a time, ceil for odd count
    - Height of the trip would be lastFloor-floor (distance travelled)
    - Take two trips (to last floor and back to that floor)
- Sum up numTrips * 2 * height for all floors, excluding last floor
'''