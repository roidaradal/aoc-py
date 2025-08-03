# Advent of Code 2017 Day 25
# John Roy Daradal 

from aoc import *

Rule = tuple[int, int, str]
RulePair = tuple[Rule, Rule]

def data(full: bool) -> tuple[str, int, dict[str, RulePair]]:
    lines = [line.strip('.:') for line in readLines(17, 25, full)]
    state = splitStr(lines[0], None)[-1]
    steps = int(splitStr(lines[1], None)[-2])
    rules: dict[str, RulePair] = {}
    for i in range(2, len(lines), 10):
        key = splitStr(lines[i+1], None)[-1]
        rule0 = createRule(lines[i+3:i+6])
        rule1 = createRule(lines[i+7:i+10])
        rules[key] = (rule0, rule1)
    return state, steps, rules

def createRule(lines: list[str]) -> Rule:
    out = int(splitStr(lines[0], None)[-1])
    step = 1 if splitStr(lines[1], None)[-1] == 'right' else -1 
    state = splitStr(lines[2], None)[-1]
    return (out, step, state)

def solve() -> Solution:
    state, steps, rules = data(full=True)
    tape: dict[int, int] = defaultdict(int)
    head: int = 0
    for _ in range(steps):
        idx = tape[head]
        out, step, state = rules[state][idx]
        tape[head] = out 
        head += step 

    count = sum(tape.values())
    return newSolution(count, "")

if __name__ == '__main__':
    do(solve, 17, 25)

'''
Solve:
- A rule is represented by the (outputValue, moveDirection, nextState)
    - Output value is what we put it in the current tape the head is pointing at 
    - Move direction (-1 for left, 1 for right) is how we move the tape head
    - Next state tells us which state to transition to next 
- For each state, there is a rule pair: what to do when the current tape head value is 0 or 1
- Start at the given starting state, and run the Turing machine for the specified number of steps
- The tape head starts at index 0, and the tape contents are all 0 by default
- Get which rule to follow based on the current state and the current value being read by the tape head
- Update the tape head's value, the new current state, and the tape head index
- After the specified number of rounds, output the number of 1s in the tape
- No problem for Part 2
'''