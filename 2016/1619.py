# Advent of Code 2016 Day 19
# John Roy Daradal 

from aoc import *

class Elf:
    def __init__(self, number: int):
        self.id: int = number
        self.next: Elf = self 
        self.prev: Elf = self

def data(full: bool) -> int:
    return int(readFirstLine(16, 19, full))

def solve() -> Solution:
    count = data(full=True)

    # Part 1 
    elf1 = findWinnerNext(count)

    # Part 2
    elf2 = findWinnerAcross(count)

    return newSolution(elf1, elf2)

def findWinnerNext(count: int) -> int:
    head = buildDLL(count)

    # Repeat until only 1 left
    left = count 
    curr = head
    while left > 1:
        # Remove next node 
        rem = curr.next 
        nxt = rem.next
        prev = rem.prev 
        prev.next = nxt 
        nxt.prev = prev 
        left -= 1
        # Move to next node
        curr = curr.next
    return curr.id

def findWinnerAcross(count: int) -> int:
    head = buildDLL(count)

    # Get across node 
    gap = count // 2 
    across = head 
    for _ in range(gap): across = across.next 

    # Repeat until only 1 left 
    left = count 
    curr = head 
    while left > 1:
        # Remove across node 
        nxt = across.next 
        prev = across.prev 
        prev.next = nxt 
        nxt.prev = prev 
        left -= 1
        needGap = left // 2
        # Update across pointer to next 
        across = nxt
        curr = curr.next 
        # Moving the current pointer reduces the gap 
        gap -= 1
        # If needed gap is not satisfied, move across pointer forward until satisfied
        while gap != needGap:
            across = across.next
            gap += 1
    return curr.id

def buildDLL(count: int) -> Elf:
    head = Elf(1)
    prev = head
    for number in range(2, count+1):
        curr = Elf(number)
        prev.next = curr 
        curr.prev = prev 
        prev = curr 
    # Link last number 
    prev.next = head 
    head.prev = prev 
    return head

if __name__ == '__main__':
    do(solve, 16, 19)

'''
Part1:
- Build the DLL containing Elf 1 to Elf N: use DLL for easy removing of items in between 
- Starting with Elf 1, repeat until only 1 elf left: 
- Remove the current's next node from the DLL
- Move to current's next node
- Output the ID of the remaining elf

Part2:
- Build the DLL similar to Part 1
- Instead of removing the next node, we'll remove the node across 
- The node across the current node is halfway away from it (e.g. if 10 nodes, curr = 0, across = 5)
- Keep track of both the current node and the across node, and their current gap 
- Starting with Elf 1, repeat until only 1 elf left:
- Remove the across node; reduce the elves left and recompute the needed gap for across 
- After removing the across node, the new across will be the old across' next node 
- Move to the current's next node 
- By moving the current pointer forward, it reduces the gap with across by 1
- Check if the current gap doesn't satisfy the needed gap
- If not, move the across pointer forward (and increase the gap) until the needed gap is satisfied
- Output the ID of the remaining elf
'''