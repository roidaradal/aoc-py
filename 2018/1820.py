# Advent of Code 2018 Day 20
# John Roy Daradal 

from aoc import *

def data(full: bool) -> str:
    return readFirstLine(18, 20, full).strip('^$')

def solve() -> Solution:
    pattern = data(full=True)

    sp: dict[coords,int] = defaultdict(lambda: sys.maxsize)
    sp[(0,0)] = 0
    points: list[coords] = [(0,0)]
    resolvePattern(pattern, points, sp)

    # Part 1
    maxDist = max(sp.values())

    # Part 2 
    count = sum(1 for dist in sp.values() if dist >= 1000)

    return newSolution(maxDist, count)

deltaOf: dict[str,delta] = {'N' : U, 'S' : D, 'W' : L, 'E' : R}

def visitNext(curr: coords, step: str, sp: dict[coords,int]) -> coords:
    nxt = move(curr, deltaOf[step])
    if sp[nxt] > sp[curr] + 1:
        sp[nxt] = sp[curr] + 1 
    return nxt

def resolvePattern(pattern: str, starts: list[coords], sp: dict[coords,int]) -> list[coords]:
    i, limit = 0, len(pattern)
    points = starts[:]
    while i < limit:
        step = pattern[i]
        if step == '(': 
            closer = findCloser(pattern, i)
            points = resolveBranches(pattern[i:closer+1], points, sp)
            i = closer + 1 # skip the resolved branch
        else: 
            for p in range(len(points)):
                points[p] = visitNext(points[p], step, sp)
            i += 1
    return points

def resolveBranches(pattern: str, starts: list[coords], sp: dict[coords,int]) -> list[coords]:
    # Pattern is (A|B|C), start processing at index 1 (skip initial open parens)
    # Important: deduplicate the list of coords before returning
    points: list[coords] = []
    for branch in segmentBranch(pattern):
        points += resolvePattern(branch, starts, sp) 
    return list(set(points))

def segmentBranch(pattern: str) -> list[str]:
    # Pattern is (A|B|C), remove the open/close parens
    pattern = pattern[1:-1] # remove the parens
    branches: list[str] = []
    branch: list[str] = []
    i, limit = 0, len(pattern)
    depth = 0 
    while i < limit:
        char = pattern[i]
        if char == '|' and depth == 0:
            branches.append(''.join(branch))
            branch = [] # reset branch 
            i += 1
            continue
        elif char == '(':
            depth += 1 
        elif char == ')':
            depth -= 1
        branch.append(char)
        i += 1
    branches.append(''.join(branch))
    return branches

if __name__ == '__main__':
    do(solve, 18, 20)

'''
Solve:
- Initialize the shortest path distance (sp) table: 
    - sp[(0,0)] = 0
    - The reset: INF (sys.maxsize for int), use defaultdict for lazy building
    - This gets updated when we visit the next room
    - Update only if sp[curr] + 1 < sp[nxt]: we can improve the current shortest path 
      for next by going coming from curr and going through 1 door
- Call resolvePattern on the whole pattern, with one starting point at (0,0):
    - It scans the text one character at a time, sometimes jumping over groups 
    - If char is NEWS, update the current points by applying the delta (use visitNext to update the SP table too)
    - If we find a group (we see an open parens), find the closing parentheses of this branch and 
      call resolveBranches on this portion
    - The resulting points after resolving the branches becomes the current set of points 
    - If we see a group, we jump over the group and go to the character after the closing parens
    - Return the current set of points, as this is also called recursively by resolveBranch
- To resolveBranches on pattern (A|B|C), we first segment the pattern into branches
- Then, we recursively call resolvePattern on each branch, starting with the passed in starting points
- Deduplicate the combined list of resulting coords to avoid duplicate computations later
- To find the closing parentheses, increase the depth if we see another ( and decrease the depth if we see its 
  matching ). Only return the index of the found ) if we see it on depth 0. This is to avoid prematurely returning 
  a closing parens that belongs to a subgroup and not to the main group being processed
- To segment a branch (A|B|C):
    - First remove the parens, then process each character 
    - Increase the depth when we see ( and decrease the depth when we see ) (similar to finding closing parens)
    - This is to avoid segmenting on inner subgroups 
    - If we see | on depth 0, then we have segmented one part of the branch: 
      we add it to the list of branches and reset the branch to empty 
    - Otherwise, we keep growing the current branch by adding the seen chars to it
    - Add the last branch to the branches list
- For Part 1, find the maximum distance among the shortest path distances to rooms
- For Part 2, count the number of shortest path distances that are at least 1,000
'''