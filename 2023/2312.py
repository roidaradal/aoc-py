# Advent of Code 2023 Day 12
# John Roy Daradal 

import re
from functools import cache
from aoc import *

def data(full: bool) -> list[str2]:
    def fn(line: str) -> str2:
        pattern, tail = line.split()
        sizes = toIntList(tail, ',')
        goal = '.'.join('#' * size for size in sizes)
        return (pattern, goal)
    return [fn(line) for line in readLines(23, 12, full)]

def solve() -> Solution:
    springs = data(full=True)

    # Part 1 
    total1 = countTotalSprings(springs, False)

    # Part 2 
    total2 = countTotalSprings(springs, True)

    return newSolution(total1, total2)

def countTotalSprings(springs: list[str2], expand: bool) -> int:
    total = 0 
    for pattern,goal in springs:
        # Compress multiple dots into one 
        pattern = compress(pattern)

        # Expand if needed
        if expand:
            pattern = '?'.join([pattern] * 5)
            goal = '.'.join([goal] * 5)
        
        # Remove extra dots on front/back
        pattern = pattern.strip('.')

        total += countPossible(pattern, goal)
    return total

def compress(text: str) -> str:
    return re.sub(r'\.+', '.', text)

@cache
def countPossible(pattern: str, goal: str) -> int:
    patLen  = len(pattern)
    goalLen = len(goal)   
    unknown = pattern.count('?')

    # Pattern shorter than goal = Infeasible
    if patLen < goalLen: 
        return 0
    
    # Pattern same length as goal = check aligned 
    if patLen == goalLen:
        for i in range(patLen):
            # skip ?, will just take the goal's value
            if pattern[i] == '?': continue 
            if pattern[i] != goal[i]:
                return 0 # not aligned 
        return 1 # all aligned
    
    # If goal is empty, check that there are no # in pattern 
    if goalLen == 0:
        return 1 if pattern.count('#') == 0 else 0
    
    # If no unknown, check if pattern == goal 
    if unknown == 0:
        return 1 if pattern == goal else 0
    
    idx = pattern.index('?')
    pattern1 = pattern[:idx] + '#' + pattern[idx+1:]
    pattern2 = pattern[:idx] + '.' + pattern[idx+1:]
    pattern2 = compress(pattern2).strip('.')

    # Process pattern1 and pattern2 
    total = 0
    for nxtPattern in [pattern1, pattern2]:
        count = 0
        if unknown == 1: 
            # replaced the last ?, compare pattern and goal
            count = 1 if nxtPattern == goal else 0
        else: # has more ?, check prefix
            idx = nxtPattern.index('?')
            origPrefix = nxtPattern[:idx]
            prefix = origPrefix 
            if len(goal) < len(prefix): # prefix must have extra '.'
                prefix = prefix.strip('.')
            isValid = goal.startswith(prefix)
            if isValid: 
                nxtGoal = goal
                if origPrefix.endswith('.'): # matched a full group = prune
                    nxtPattern = nxtPattern[idx:]
                    nxtGoal = nxtGoal[idx:]
                count = countPossible(nxtPattern, nxtGoal)
        total += count 
    return total

if __name__ == '__main__':
    do(solve, 23, 12)

'''
Solve: 
- To create the goal, join # blocks of the given size by .
- For Part 1, compress the pattern and remove the front/back extra dots 
- For Part 2, compress the pattern, expand pattern and goal 5x, and remove pattern front/back extra dots
- To compress a pattern, replace multiple dots with a single dot 
- To expand the pattern, join 5 copies of the original pattern by ?
- To expand the goal, join 5 copies of the original goal by .
- Return the total possibility counts for all springs

CountPossible:
- Use functools.cache to memoize the results (avoid recomputation of previously seen pattern/goal)
- If pattern length < goal length = infeasible, return 0 
- If pattern and goal has same length = check that they only differ because of ? 
- If goal is empty, check that there are no remaining # in the pattern (only ? or .)
- If no more ?, check if pattern == goal (exact match)
- Form pattern1 and pattern2 by replacing the first ? with # and ., respecively 
- For pattern2, compress it (because .. could've been formed) and strip leading/trailing .
- Do this for both pattern1 and pattern2, then return their total:
    - If no more ? left, do exact match 
    - If has ? left, get the prefix => until the ? index
    - Remove the extra . if the prefix is longer than the goal (e.g. #. vs #)
    - Check if still a valid prefix by checking if the goal starts with the prefix
    - If not valid, count = 0 
    - If the original prefix ends with ., we have matched a full group so we can prune it
    - Adjust the next pattern and goal by starting only after the . 
    - Example: From ##.#?, we match ##. as the prefix, so we can continue with #? only
    - Recursively call countPossible on the next pattern and goal
'''