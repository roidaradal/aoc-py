# Advent of Code 2018 Day 14
# John Roy Daradal 

from aoc import *

def data(full: bool) -> int:
    line = readLines(18, 14, full)[0]
    return int(line)

def part1():
    steps = data(full=True)
    limit = steps + 10
    a, b = 0, 1
    scores = [3, 7]
    while len(scores) < limit:
        total = scores[a] + scores[b]
        for d in str(total):
            scores.append(int(d))
        s = len(scores)
        a = (a + 1 + scores[a]) % s 
        b = (b + 1 + scores[b]) % s 
    output = ''.join(str(x) for x in scores[steps:limit])
    print(output) 

def part2():
    goal = str(data(full=True))
    N = len(goal)
    M = N+1 
    a, b = 0, 1 
    scores = [3, 7]
    while True:
        total = scores[a] + scores[b]
        for d in str(total):
            scores.append(int(d))
        # move forward 
        s = len(scores)
        a = (a + 1 + scores[a]) % s 
        b = (b + 1 + scores[b]) % s 
        # Check suffix 
        if len(scores) < N: continue 
        suffix = ''.join(str(x) for x in scores[-M:])
        if suffix.startswith(goal):
            print(len(scores)-M)
            break
        elif suffix.endswith(goal):
            print(len(scores)-N)
            return 

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Input data is number of recipes; limit is 10 + this number (score the next 10 recipes)
- Start with two recipes: 3, 7 
- Loop until we fill up the limit number of recipes
- To create new recipe scores, combine the two current recipe scores and add their digits to the scores list 
- The two elves step forward by adding 1 + current score to current index, with wrap-around
- After having enough scores, concatenate the scores from the input number to limit

Part2:
- Similar processing to Part 1; but look for the first time the input data appears in the scores list
- Check the suffix of the current scores list 
- The suffix could start with the goal or end with the goal (off by one)
- If goal is found, output the appropriate number of items to the left of the found score sequence
'''