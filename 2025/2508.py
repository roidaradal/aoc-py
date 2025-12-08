# Advent of Code 2025 Day 08
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int3]:
    return [toInt3(line,',') for line in readLines(25, 8, full)]

def solve() -> Solution:
    points = data(full=True)
    pairLimit = 1000
    numPoints = len(points)

    # Create point pairs and their Euclidean distances 
    pairs = [
        (points[i], points[j], euclidean3(points[i], points[j]))
        for i in range(numPoints)
        for j in range(i+1, numPoints)         
    ]
    pairs.sort(key=lambda p: p[2]) # sort by ascending distance 

    groupOf: dict[int3, int] = {}
    inGroup: dict[int, list[int3]] = {}
    group = 0
    size, length = 0, 0
    allGrouped = False
    for i, (p1, p2, _) in enumerate(pairs):
        hasGroup1, hasGroup2 = p1 in groupOf, p2 in groupOf
        if hasGroup1 and hasGroup2: # both already has group
            group1, group2 = groupOf[p1], groupOf[p2]
            if group1 != group2: # merge 
                for pt in inGroup[group2]:
                    groupOf[pt] = group1
                inGroup[group1].extend(inGroup[group2])
                del inGroup[group2]
        elif hasGroup1: # only p1 has group
            groupOf[p2] = groupOf[p1]
            inGroup[groupOf[p1]].append(p2)
        elif hasGroup2: # only p2 has group
            groupOf[p1] = groupOf[p2]
            inGroup[groupOf[p2]].append(p1)
        else: # both no group
            groupOf[p1] = group 
            groupOf[p2] = group 
            inGroup[group] = [p1, p2]
            group += 1

        # Part 1
        if i == pairLimit-1: 
            s1, s2, s3 = sorted([len(pts) for pts in inGroup.values()], reverse=True)[:3]
            size = s1 * s2 * s3 

        # Part 2
        # Stop condition: all points have group, and only 1 group left
        if not allGrouped:
            allGrouped = len(groupOf) == numPoints
        if allGrouped and len(set(groupOf.values())) == 1:
            length = p1[0] * p2[0] # multiply x values of points that made circuit whole
            break 

    return newSolution(size, length)

if __name__ == '__main__':
    do(solve, 25, 8)

'''
Solve:
- Create point pairs and compute their Euclidean distances 
- Sort the pairs by ascending distance
- Go through each pair of points:
    - If both points already has group but are different groups,
      merge them by converting all of points in group2 be part of group1 
    - If only 1 of the points has a group, bring the other point to the group
    - If both have no groups, create a new group with the points as members
- For Part 1, after processing the first 1000 shortest distance pairs:
    - Find the 3 largest groups and multiply their sizes 
    - Output the product of their sizes
- For Part 2, check if the points have formed one group:
    - If so, multiply the x-values of the current points which made the circuit whole
    - Output the product of the x-values
'''