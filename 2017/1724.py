# Advent of Code 2017 Day 24
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int3]:
    def fn(line: str, idx: int) -> int3:
        a,b = toInt2(line, '/')
        return (idx, a, b)
    return [fn(line, idx) for idx, line in enumerate(readLines(17, 24, full))]

def solve() -> Solution:
    items = data(full=True)

    starters: list[int3] = []
    for item in items:
        if item[1] == 0:
            starters.append(item)
        elif item[2] == 0:
            starters.append(flipped(item))

    q: list[list[int3]] = []
    for starter in starters:
        q.append([starter])

    maxStrength1 = 0
    maxStrength2, maxLength = 0, 0 
    while len(q) > 0:
        bridge = q.pop(0)
        
        nxtItems = getValidConnections(bridge, items)
        if len(nxtItems) == 0: # end bridge here
            # Part 1
            strength = bridgeStrength(bridge)
            maxStrength1 = max(maxStrength1, strength)

            # Part 2 
            bridgeLength = len(bridge)
            if bridgeLength > maxLength:
                maxLength = bridgeLength 
                maxStrength2 = strength
            elif bridgeLength == maxLength:
                maxStrength2 = max(maxStrength2, strength)
        else:
            for nxt in nxtItems:
                q.append(bridge + [nxt])

    return newSolution(maxStrength1, maxStrength2)

def flipped(item: int3) -> int3:
    i,a,b = item 
    return (i,b,a)

def bridgeStrength(bridge: list[int3]) -> int:
    return sum(p[1] + p[2] for p in bridge)

def getValidConnections(bridge: list[int3], items: list[int3]) -> list[int3]:
    nxtItems: list[int3] = []
    done: list[int] = [p[0] for p in bridge]
    tail = bridge[-1][2] # ending port 
    for item in items:
        if item[0] in done: continue 
        if item[1] == tail:
            nxtItems.append(item)
        elif item[2] == tail:
            nxtItems.append(flipped(item))
    return nxtItems

if __name__ == '__main__':
    do(solve, 17, 24)

'''
Solve:
- Represent items as triple (idx,x,y) - idx is used to preserve identity of the item even in its 
  flipped state, so that (5,1,2) and (5,2,1) refers to the same item (#5) even when 1/2 and 2/1 are flipped
- Find the starter items: 0/x or x/0, convert to canonical form 0/x (flip if not)
- Use a queue to process bridges (connected items); initialize with the starters
- For Part 1, find the strength of the strongest bridge you can create
- For Part 2, find the maximum strength of the longest bridge you can create
- Bridge strength is the sum of x+y for all x/y items in the bridge
- For the current bridge, get the valid possible connections to extend the bridge:
    - The bridge tail is the path's last item's ending port y (x/y)
    - Check the other items that are not yet in the bridge
    - If the item starts or ends (flip item) with the tail, add it as a valid connection
- If there are no more valid connections, the current bridge ends here:
    - Update the max strength, if necessary, for Part 1
    - Update the max length, and the max strength at that length, if necessary, for Part 2
- Otherwise, we add the valid connections as new bridges to the queue
'''