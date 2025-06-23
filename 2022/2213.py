# Advent of Code 2022 Day 13
# John Roy Daradal 

import json, functools
from aoc import *

Pair = tuple[list,list]

def data(full: bool) -> list[Pair]:
    pairs: list[Pair] = []
    lines = readLines(22, 13, full)
    for i in range(0, len(lines), 3):
        l1 = json.loads(lines[i])
        l2 = json.loads(lines[i+1])
        pairs.append((l1, l2))
    return pairs

def solve() -> Solution:
    pairs = data(full=True)

    # Part 1 
    total = 0
    for i, (l1, l2) in enumerate(pairs):
        if compareLists(l1, l2) == -1: # L1 must be smaller than L2
            total += i+1
    
    # Part 2 
    div1 = [[2]]
    div2 = [[6]]
    packets: list[list] = []
    for l1,l2 in pairs:
        packets.append(l1)
        packets.append(l2)
    packets.append(div1)
    packets.append(div2)
    packets.sort(key=functools.cmp_to_key(compareLists))
    idx1 = packets.index(div1) + 1 
    idx2 = packets.index(div2) + 1
    decoderKey = idx1 * idx2

    return newSolution(total, decoderKey)

def compareLists(l1: list, l2: list) -> int:
    # Check for empty lists
    n1, n2 = len(l1), len(l2)
    if n1 == 0 and n2 == 0:
        return 0
    elif n1 == 0: # left side run out of values first
        return -1 
    elif n2 == 0: # right side run out of values first
        return 1
    
    # Compare first items 
    v1, v2 = l1[0], l2[0]
    t1, t2 = type(v1), type(v2)

    cmp1 = 0
    if t1 == int and t2 == int:
        cmp1 = cmp(v1, v2)
    elif t1 == list and t2 == list:
        cmp1 = compareLists(v1, v2)
    elif t1 == int and t2 == list:
        cmp1 = compareLists([v1], v2)
    elif t1 == list and t2 == int:
        cmp1 = compareLists(v1, [v2])
    
    if cmp1 != 0:
        return cmp1 
    else:
        return compareLists(l1[1:], l2[1:])

if __name__ == '__main__':
    do(solve, 22, 13)

'''
Solve:
- In loading data, load the lists using JSON, add as list pairs
- For Part 1, compare the list pairs; if left pair is smaller than right pair, 
  add the 1-based index of the pair to the total
- For Part 2, combine all pairs into one list of packets, and add the 2 dividers 
- Sort the list of packets using the list comparison function
- Find the two dividers' 1-based index in the sorted list 
- Return the product of the 2 indexes

CompareLists:
- Check for empty lists
    - if both are empty = 0
    - if left is empty (run out of values first) = -1
    - if right is empty (run out of values first) = 1 
- We can now compare the first items (sure either are not empty)
- If both first items are ints, compare the numbers 
- If both first items are lists, recursively call compare list 
- If one is an int and the other is a list, call compare list with the int inside a list (x => [x])
- If the first comparison yields a 0 (tie), continue to the next item 
  by recursively calling compare list but from list[1:] of both sides
'''