# Advent of Code 2022 Day 11
# John Roy Daradal 

import operator
from aoc import *

class Monkey:
    def __init__(self, name: int):
        self.name: int = name 
        self.count: int = 0
        self.items: dict[int,int] = defaultdict(int)
        self.opFn: Callable = lambda x: x 
        self.opVal: int = 0 
        self.modTest: int = 1 
        self.throwTrue: int = 0 
        self.throwFalse: int = 0

    def inspectItems(self, relief: int, valueMod: int) -> list[int3]: # (monkeyID, item, count)
        out: list[int3] = []
        for item, count in self.items.items():
            value = self.opFn(item, self.opVal) // relief 
            if valueMod > 1: value = value % valueMod 

            divisible = value % self.modTest == 0 
            recipient = self.throwTrue if divisible else self.throwFalse 
            out.append((recipient, value, count))
            self.count += count
        self.items = defaultdict(int) # clear items after inspecting everything
        return out

def data(full: bool) -> list[Monkey]:
    operation = {
        '+' : operator.add, 
        '*' : operator.mul,
        '^' : operator.pow,
    }
    monkeys: list[Monkey] = []
    m = Monkey(0)
    for line in readLines(22, 11, full):
        if line.startswith('Monkey'): 
            continue 
        elif line.startswith('Starting items'):
            items = toIntList(splitStr(line, ':')[1], ',')
            for item in items:
                m.items[item] += 1
        elif line.startswith('Operation'):
            _, op, val = splitStr(splitStr(line, '=')[1], None)
            if val == 'old':
                k = '^' if op == '*' else '*'
                m.opFn = operation[k]
                m.opVal = 2 
            else:
                m.opFn = operation[op]
                m.opVal = int(val)
        elif line.startswith('Test'):
            m.modTest = lastNumber(line)
        elif line.startswith('If true'):
            m.throwTrue = lastNumber(line)
        elif line.startswith('If false'):
            m.throwFalse = lastNumber(line)
        elif line == '':
            monkeys.append(m)
            m = Monkey(len(monkeys))
    monkeys.append(m)
    return monkeys

def solve() -> Solution:
    # Part 1 
    monkeys = data(full=True)
    rounds, relief, valueMod = 20, 3, 1
    level1 = monkeyThrows(monkeys, rounds, relief, valueMod)

    # Part 2
    monkeys = data(full=True)
    rounds, relief, valueMod = 10_000, 1, 1 
    for m in monkeys: valueMod *= m.modTest
    level2 = monkeyThrows(monkeys, rounds, relief, valueMod)

    return newSolution(level1, level2)

def monkeyThrows(monkeys: list[Monkey], rounds: int, relief: int, valueMod: int) -> int:
    for _ in range(rounds):
        for m in monkeys:
            result = m.inspectItems(relief, valueMod)
            for i,item,count in result:
                monkeys[i].items[item] += count 

    monkeys = sorted(monkeys, key=lambda m: m.count, reverse=True)
    m1, m2 = monkeys[0], monkeys[1]
    return m1.count * m2.count

def lastNumber(line: str) -> int:
    return int(line.split()[-1])

if __name__ == '__main__':
    do(solve, 22, 11)

'''
Solve:
- Repeat for indicated number of rounds:
    - For each monkey, it inspects its items and distributes to other monkeys using the given relief factor and valueMod 
    - Process the result of the monkey's inspection: distribute to recipient monkeys the item and their count
- Monkey inspect items:
    - For each (item, count) of monkey's current items, compute the new value by applying the operation to the 
    current item and dividing by the relief factor 
    - If valueMod is more than 1, reduce the value by applying modulo valueMod 
    - Decide where to throw (throwTrue/throwFalse) by checking if new value is cleanly divisible by the monkey's modTest value 
    - Increment the monkey's counter by the count of items 
    - Clear the monkey's items after inspection
- Get the top2 monkeys with most inspected items; return the product of their counts
- For Part 1, run for 20 rounds, with relief factor = 3, and valueMod = 1 (dont reduce)
- For Part 2, run for 10k rounds, with relief factor = 1, and valueMod = product of monkey.modTest values
    - BigInt % productOfModTests would still be the same answer; this keeps the worry levels from being too big
    - Works because the operation for deciding where the value ends up in (throwTrue/throwFalse) is also modulo
      and the actual values the monkeys hold/throw doesn't matter, only the count of inspections
'''