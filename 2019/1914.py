# Advent of Code 2019 Day 14
# John Roy Daradal 

import math
from aoc import *

Book = dict[strInt, list[strInt]]

def data(full: bool) -> Book:
    book: Book = {}
    for line in readLines(19, 14, full):
        if line == '': break
        head, tail = splitStr(line, '=>')
        k = ingredient(tail)
        v = [ingredient(x) for x in splitStr(head, ',')]
        book[k] = v
    return book

def ingredient(line: str) -> strInt:
    qty, item = line.split()
    return (item, int(qty))

def solve() -> Solution:
    book = data(full=True)

    # Part 1 
    minOre = requiredOre(book, 1)

    # Part 2
    stockOre = 1_000_000_000_000
    fuelQty = stockOre // minOre 
    jump = 1_000_000

    while True:    
        needOre = requiredOre(book, fuelQty)
        if needOre > stockOre:
            fuelQty -= jump 
            if jump == 1:
                break
            else:
                jump = jump // 10
        else:
            fuelQty += jump

    return newSolution(minOre, fuelQty)

def requiredOre(book: Book, fuelQty: int) -> int:
    ore = 0
    q: list[strInt] = [('FUEL', fuelQty)]
    extra: dict[str, int] = defaultdict(int)
    while len(q) > 0:
        material, needQty = q.pop(0)

        if material == 'ORE':
            ore += needQty 
            continue

        # Check if can take from extra material
        extraQty = extra[material]
        takeFromExtra = min(extraQty, needQty)
        extra[material] -= takeFromExtra
        needQty -= takeFromExtra
        if needQty == 0: continue

        # Find replacement in the book 
        for key, replacements in book.items():
            mat, qty = key
            if mat != material: continue

            repeat = math.ceil(needQty / qty)
            for repMat, repQty in replacements:
                q.append((repMat, repQty * repeat))
            totalQty = qty * repeat 
            extra[material] += totalQty - needQty
            break

    return ore


if __name__ == '__main__':
    do(solve, 19, 14)

'''
Solve:
- For Part 1, find the minimum ore needed to produce 1 fuel 
- For Part 2, we have 1 trillion stocks of ore; figure out the maximum amount of fuel we can make 
- Start with fuelQty at 1 trillion / minOre to produce 1 fuel (from Part 1)
- Start with jump amount at 1 million
- Compute the needed ore for the current fuelQty:
    - If it doesn't exceed the stock ore, increment fuelQty by jump and try again
    - If it exceeds, go back to the previous amount, and divide the jump by 10 (smaller increment)
    - Eventually, the jump goes to 1 (similar idea to jump search)
    - If we exceed the stock ore and jump is already at 1, we stop the loop

RequiredOre:
- Start with the required FUEL qty on the queue, and work backwards to count the required ore 
- Keep track of extra ingredients left over during the conversion 
- Dequeue a material and its qty from the queue for replacement 
- If the dequeued material is ORE, we add the qty to the total ore counter 
- Otherwise, check first if there is extra material we can use 
- Reduce the needed qty by the extra material available (if any)
- If needed qty falls to 0, can now continue to next item 
- Find the replacement items from the recipe book 
- Based on the recipe qty of the material, figure out how many times to repeat the replacements (take ceiling)
- Add the repeated replacement items to the end of the queue 
- Add to extra material counter if any left over from the replaced item
'''