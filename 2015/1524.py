# Advent of Code 2015 Day 24
# John Roy Daradal 

import itertools
from functools import reduce
from operator import mul
from aoc import *

Combo = tuple[int,...]

def data(full: bool) -> list[int]:
    return [int(line) for line in readLines(15, 24, full)]

def solve() -> Solution:
    items = data(full=True)

    # Part 1
    score1 = findBestDivide(items, 3)

    # Part 2
    score2 = findBestDivide(items, 4)

    return newSolution(score1, score2)

def findBestDivide(items: list[int], numGroups: int) -> int:
    goalSum = sum(items) // numGroups

    # Base case: 1 item
    comboDeficit: dict[int, dict[int, set[Combo]]] = {}
    comboDeficit[1] = defaultdict(set)
    for x in items:
        deficit = goalSum - x 
        comboDeficit[1][deficit].add((x,))

    n = 2
    while True:
        comboDeficit[n] = defaultdict(set)
        for deficit, combos in comboDeficit[n-1].items():
            for combo in combos:
                for x in items:
                    if x in combo: continue # skip duplicate item
                    if x > deficit: continue # skip if adding x to combo exceeds the goalSum
                    key = tuple(sorted(combo + (x,)))
                    deficit2 = deficit - x 
                    comboDeficit[n][deficit2].add(key)

        if 0 in comboDeficit[n]:
            for combo in sorted(comboDeficit[n][0]):
                if isDividable(items, goalSum, combo, numGroups-1):
                    return reduce(mul, combo)
                
        n += 1

def isDividable(items: list[int], goalSum: int, combo: Combo, numGroups: int) -> bool:
    others: list[int] = [x for x in items if x not in combo]
    for indexes in itertools.product(range(numGroups), repeat=len(others)):
        groupSums: list[int] = []
        for groupID in range(numGroups):
            groupSum = sum(others[idx] for idx,group in enumerate(indexes) if group == groupID)
            groupSums.append(groupSum)
        if all(groupSum == goalSum for groupSum in groupSums):
            return True
    return False

if __name__ == '__main__':
    do(solve, 15, 24)

'''
Solve: 
- For Part 1, find best division for 3 groups
- For Part 2, find best division for 4 groups
- The goal sum is the sum of items / numGroups, since all groups should have equal weight
- We will go through combos of size 1,2,3,..., taking note of the combo and their deficit towards the goalSum
- Start with comboSize=1: individual items; the deficit is simply the goalSum - item
- Then we start from comboSize=2, and increase it until we find a solution
- For the current comboSize, we'll look at the comboSize-1's comboDeficits, and add 1 item to it
- Go through each combo, and each item: this should form the comboSize from comboSize-1 + 1
- If the item is already in the combo, skip it (no duplicates)
- If the item exceeds the duplicate, skip it (combo sum will exceed goal sum)
- Create the new combo by adding the item to the smaller combo: sort the tuple so that we get unique combos
- The deficit of the new combo = oldDeficit - item
- After processing the new combos for the current comboSize, check if 0 is in the list of deficits:
- Deficit = 0 means that the sum of this combo = goal sum 
- Go through the combos with deficit=0 in ascending order, so that the first valid one is the one we return
- Check if the remaining items, excluding the combo items, can also be divided into the rest of the groups
  such that the group sums are also goal sum
- The first combo that is dividable will have the smallest score, so return the product of the combo
- To check if the remaining items are dividable into numGroups-1:
    - Let others = items that are not in combo 
    - To create groupings, we use product(range(numGroups), repeat=len(others))
    - Example: 2 groups => product([0,1], repeat=numOthers)
    - We use the group number to group the items together, then go through the sums of each group
    - If all group sums == goal sum, then it is dividable
'''