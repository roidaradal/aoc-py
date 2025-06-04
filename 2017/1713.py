# Advent of Code 2017 Day 13
# John Roy Daradal 

from aoc import *

# pos, range, delta
Scanners = dict[int, int3]

def data(full: bool) -> Scanners:
    scanner: Scanners = {}
    for line in readLines(17, 13, full):
        k, r = toIntList(line, ':')
        scanner[k] = (0, r, 1)
    return scanner

def solve():
    scanner = data(full=True)
    limit = max(scanner.keys()) + 1

    T: dict[int,Scanners] = {}
    T[0] = scanner 
    for t in range(1, limit):
        T[t] = nextState(T[t-1])
    
    penalty = getPenalty(T, 0, limit)
    print(penalty)

    delay = 0
    while True:
        t = limit + delay 
        T[t] = nextState(T[t-1])
        penalty = getPenalty(T, delay, limit, stopIfCaught=True)
        if penalty == 0:
            print(delay)
            break
        del T[delay] # remove previous head, to keep T from growing too big
        delay += 1

def nextState(scanner: Scanners) -> Scanners:
    scanner2: Scanners = {}
    for k in scanner:
        pos, r, move = scanner[k]
        if pos == 0:
            pos += 1
            move = 1
        elif pos == r-1:
            pos -= 1
            move = -1 
        else:
            pos += move 
        scanner2[k]  = (pos, r, move)
    return scanner2 

def getPenalty(T: dict[int,Scanners], start: int, limit: int, stopIfCaught: bool = False) -> int:
    penalty = 0 
    for layer in range(limit):
        t = start + layer 
        if layer not in T[t]: continue 
        scanPos, scanRange, _ = T[t][layer]
        if scanPos == 0:
            penalty += layer * scanRange 
            if stopIfCaught:
                return 1 # need non-zero return; cannot return penalty because if at layer 0, penalty = 0
    return penalty

if __name__ == '__main__':
    do(solve)

'''
Part1:
- Simulate the scanner states from t=0 up to limit (max scanner key)
- Store the scanner states in timelapse map for easier accessing during simulation
- To produce the next state, move each scanner forward/backward (depending on their current direction),
  if they reach the front: bounce forward (change direction)
  if they reach the end of scanner: bound backward (change direction)
- Compute the penalty of starting at t=0:
    - Each layer will be visited at t= start + layer (there could be delays for start)
    - From the memoized time states, get the position and range of the scanner at that layer, at that time 
    - If scanner at position 0, we are caught; add penalty (layer * scanRange)
    - Can stop immediately if stopIfCaught flag is on
    - Return the total penalty from traversing all layers

Part2:
- Find the minimum delay time that produces penalty 0 
- Produce one new state, add to T, and remove the oldest after each iteration (to prevent from going too big)
- Safe to delay the previous head because next simulations won't start there 
- Compute the penalty of starting at current delay 
- Stop if we find a delay time that gives penalty 0
'''