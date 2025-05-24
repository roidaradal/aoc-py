# Advent of Code 2020 Day 06
# John Roy Daradal 

from aoc import *

Group = list[str]

def data(full: bool) -> list[Group]:
    groups: list[Group] = []
    curr: Group = []
    for line in readLines(20, 6, full):
        if line == '':
            groups.append(curr)
            curr = []
        else:
            curr.append(line)
    groups.append(curr)
    return groups

def part1():
    groups = data(full=True)
    total = getTotal(groups, countYes)
    print(total) 

def part2():
    groups = data(full=True)
    total = getTotal(groups, countAllYes)
    print(total) 

def countYes(group: Group) -> int:
    qs = set()
    for questions in group:
        qs = qs.union(set(questions))
    return len(qs)

def countAllYes(group: Group) -> int:
    count = defaultdict(int)
    for questions in group: 
        for q in questions:
            count[q] += 1
    return len([k for k,v in count.items() if v == len(group)])

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Count the number of unique questions answered by the group
- Get the total for all groups

Part2:
- For each group, count the number of times each question was answered
- Count the questions where all group members answered it
- Get the total for all groups
'''