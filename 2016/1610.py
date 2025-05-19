# Advent of Code 2016 Day 10
# John Roy Daradal 

from aoc import *

class Problem:
    def __init__(self):
        self.chips = []
        self.bots  = {}

Bot = tuple[strInt, strInt] # low, high

def data(full: bool) -> Problem:
    problem = Problem()
    for line in readLines(16, 10, full):
        p = line.split()
        if p[0] == 'value':
            value, who = int(p[1]), int(p[-1])
            problem.chips.append((value, who))
        elif p[0] == 'bot':
            who = int(p[1])
            low = (p[5], int(p[6]))
            high = (p[-2], int(p[-1]))
            problem.bots[who] = (low, high)
    return problem

def solve():
    problem = data(full=True)
    chips, bots = problem.chips, problem.bots 
    goal = (17,61)
    output = defaultdict(list)
    botValues = {b: [] for b in bots}

    for value,who in chips:
        botValues[who].append(value)

    while True:
        botValues2 = {b: [] for b in bots}
        hasMovement = False
        for b,v in botValues.items():
            if len(v) == 2:
                v = sorted(v)
                if tuple(v) == goal:
                    print(b) # print out who is in charge of comparing 17,61
                for i,(dest,who) in enumerate(bots[b]):
                    if dest == 'bot':
                        botValues2[who].append(v[i])
                    else:
                        output[who].append(v[i])
                hasMovement = True
            else:
                botValues2[b] += v
        botValues = botValues2
        if not hasMovement: break
    
    a,b,c = output[0][0], output[1][0], output[2][0]
    print(a * b * c)


if __name__ == '__main__':
    do(solve)

'''
Solve:
- In reading data, separate the bot definitions and value assignments 
- Bots are defined by their low-high rules
- Initialize bots to hold the values indicated in the input data
- At each round (and at the start), make sure the bots are holding a sorted version of values (low, high)
- Repeat these steps until there are no more movements available
- Check bots with 2 values: they can move their values based on their low-high rule
- Put the low and high values to the respective bins (bot or output)
- For Part 1, check if the two values being compared are the goal; if it is, print out the bot number 
- For Part 2, wait for the bots to stop moving values and print the product of the first items in output 0,1,2
'''